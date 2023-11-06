from fastapi import Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import json
import datetime
import uvicorn
import os
import re
from google.cloud import run_v2
from google.iam.v1 import iam_policy_pb2
from lib.RUN import create_service_tagging, create_service_preview_tagging, sample_set_iam_policy
from lib.SSL import ssl_create_managed
from lib.LB import *
from lib.DomainList import domain_list
from google.cloud import datastore
import random
import string
# project_id="server-side-tagging-392006"


router = APIRouter()
client = datastore.Client()

@router.post('/create')
async def sst_create(request: Request):
    payload_bytes = await request.body()
    print(payload_bytes)
    payload_str = payload_bytes.decode("utf-8")
    queryParams = json.loads(payload_str)
    print(queryParams)

    store_id = queryParams.get('store_id')
    region = queryParams.get('region')
    domain = queryParams.get('domain')
    container_config = queryParams.get('container_config')

    

    #datastore part
    kind = 'server-side-tagging'
    parent_key=None
    custom_key = client.key(kind,str(store_id),parent=parent_key)
    entity = datastore.Entity(key=custom_key)


    print("name", store_id)
    print("region", region)
    print("container_config", container_config)

    preview_server_url, preview_name = await create_service_preview_tagging(store_id, region, container_config)
    sample_set_iam_policy(preview_name)
    result1, tagging_name, details = await create_service_tagging(store_id, region, container_config, preview_server_url)
    sample_set_iam_policy(tagging_name)

    entity["name"]=store_id
    entity['region']=region
    entity['domain']=domain
    entity['container_config']=container_config
    entity['preview_tagging_server_url']=preview_server_url
    entity['tagging_server_url']=result1
    client.put(entity)

    if domain!= None:
        certificate_name = f'sst-certificate-{generate_random_string(10)}'
        print(certificate_name)
        list_domain, certis = domain_list(domain, certificate_name)
        print("domain_list",list_domain)
        ssl_create_managed(certificate_name=certificate_name, domains=list_domain)
        print("SSL certificate create successfully")
        entity['certificate_name']=certificate_name
        client.put(entity)
        # Function to check state of newly created certificate to be added
        https_proxy_attach_ssl_certificate(certificate_urls=certis)
        # Works till here Rev: test-backend-sst-lb-00018-lrx #

        # Latest revision additions Rev: test-backend-sst-lb-00019
        cloud_run_name = f"sst-{store_id}"
        backend_service_name = f"sst-{store_id}-be-{generate_random_string(10)}"
        neg_name = f"sst-{store_id}-neg-{generate_random_string(10)}"
        print(json.dumps({"cloud_run_name": cloud_run_name, "backend_service_name": backend_service_name, "neg_name": neg_name}))
        
        neg_create_regional_cloud_run(region=region, neg_name=neg_name, cloud_run_service_name= cloud_run_name)
        entity['neg_name']=neg_name
        client.put(entity)
        backend_create_global(backend_service_name=backend_service_name, neg_name = neg_name, neg_region=region)
        entity['backend_service_name']=backend_service_name
        client.put(entity)
        hostrule_add(domain=[domain], backend_service_name=backend_service_name, paths=["/test", "/dev", "/pre-prod"])
    else:
        print('Domain name not provided')
    
    return {"Payload Details": details}

@router.post("/my-update")
async def update(request:Request):

    payload_bytes = await request.body()
    print(payload_bytes)
    payload_str = payload_bytes.decode("utf-8")
    queryParams = json.loads(payload_str)
    print(queryParams)


    store_id = queryParams.get('store_id')
    container_config = queryParams.get('container_config')
    domain = queryParams.get('domain')
    print('today_domain_check',domain)



    kind = 'server-side-tagging'
    parent_key=None
    custom_key = client.key(kind,str(store_id),parent=parent_key)
    entity = datastore.Entity(key=custom_key)

    entity["name"]=store_id
    entity['container_config']=container_config
    task_key = client.key('server-side-tagging', store_id)
    task = client.get(task_key)

    json_data={
        "domain":task.get('domain'),
        "region":task.get('region'),
        "container_config":task.get('container_config'),
        "preview_tagging_server_url":task.get('preview_tagging_server_url'),
        "tagging_server_url":task.get('tagging_server_url'),
        "certificate_name":task.get('certificate_name'),
        "neg_name":task.get('neg_name'),
        "backend_service_name":task.get('backend_service_name')
        
    }
    domain_datastore=str(json_data['domain'])
    region=str(json_data['region'])


    project_id = 'server-side-tagging-392006'
    service_name="sst-"+str(store_id)
    preview_service_name="sst-"+str(store_id)+"-preview"
    # Container config given and update
    if container_config!=None:
        store_id=queryParams.get('store_id')
        # #region=str(json_data['region'])
        domain=str(json_data['domain'])
        # container_config=str(json_data['container_config'])
        preview_tagging_server_url=str(json_data['preview_tagging_server_url'])
        tagging_server_url = str(json_data['tagging_server-url'])
        certificate_name=str(json_data['certificate_name'])
        neg_name=str(json_data['neg_name'])
        backend_service_name=str(json_data['backend_service_name'])
        entity['store_id']=store_id
        # entity['region']=region
        entity['domain']=domain
        # entity['container_config']=container_config
        entity['preview_tagging_server_url']=preview_tagging_server_url
        entity['tagging_server_url']=tagging_server_url
        entity['certificate_name']=certificate_name
        entity["neg_name"]=neg_name
        entity['backend_service_name']=backend_service_name
        client.put(entity)

        run_client = run_v2.ServicesClient()
        request=run_v2.UpdateServiceRequest(
            service = {
                
                "name" : f"projects/{project_id}/locations/{region}/services/{service_name}",
                "ingress": "INGRESS_TRAFFIC_ALL",
                "template": {
                    "scaling":{
                        "min_instance_count":1,
                        "max_instance_count":2    
                    },
                    "containers": [{
                        "image": "gcr.io/cloud-tagging-10302018/gtm-cloud-image:stable",
                        "resources": {
                            "cpu_idle": False
                        },
                        "env": [{
                            "name": "CONTAINER_CONFIG",
                            "value": container_config
                        }]
                        
                    }],
                    "timeout":{
                        "seconds": 60
                    }
                }
            }  
        )
        operation = run_client.update_service(metadata= [("name", service_name)],request=request)
        
    #Update preview server
        request_preview=run_v2.UpdateServiceRequest(
            service = {
                
                "name" : f"projects/{project_id}/locations/{region}/services/{preview_service_name}",
                "ingress": "INGRESS_TRAFFIC_ALL",
                "template": {
                    "scaling":{
                        "min_instance_count":1,
                        "max_instance_count":2    
                    },
                    "containers": [{
                        "image": "gcr.io/cloud-tagging-10302018/gtm-cloud-image:stable",
                        "resources": {
                            "cpu_idle": False
                        },
                        "env": [{
                            "name": "CONTAINER_CONFIG",
                            "value": container_config
                        }]
                        
                    }],
                    "timeout":{
                        "seconds": 60
                    }
                }
            }  
        )
        operation = run_client.update_service(metadata= [("name", preview_service_name)],request=request_preview)
        entity["name"]=store_id
        entity['region']=region
        # entity['domain']=domain
        entity['container_config']=container_config
        
    
        client.put(entity)
    else:
        print("Container config not provided")


    # print(operation.result)
    print('ds_domain',domain_datastore)

# Domain not given and update
    if domain_datastore == 'None' and domain != None:
        store_id=queryParams.get('store_id')
        region=str(json_data['region'])
        container_config=str(json_data['container_config'])
        preview_tagging_server_url=str(json_data['preview_tagging_server_url'])
        tagging_server_url = str(json_data['tagging_server-url'])
        entity['store_id']=store_id
        entity['region']=region
        entity['container_config']=container_config
        entity['preview_tagging_server_url']=preview_tagging_server_url
        entity['tagging_server_url']=tagging_server_url
        client.put(entity)
        domain = queryParams.get('domain')
        print('ud',domain)

        


        certificate_name = f'sst-{store_id}-certificate-{generate_random_string(10)}'
        print(certificate_name)
        list_domain, certis = domain_list(domain, certificate_name)
        print("domain_list",list_domain)
        ssl_create_managed(certificate_name=certificate_name, domains=list_domain)
        print("SSL certificate create successfully")
        entity['certificate_name']=certificate_name
        client.put(entity)
        # Function to check state of newly created certificate to be added
        https_proxy_attach_ssl_certificate(certificate_urls=certis)
        # Works till here Rev: test-backend-sst-lb-00018-lrx #

        # Latest revision additions Rev: test-backend-sst-lb-00019
        cloud_run_name = f"sst-{store_id}"
        backend_service_name = f"sst-{store_id}-be-{generate_random_string(10)}"
        neg_name = f"sst-{store_id}-neg-{generate_random_string(10)}"
        print(json.dumps({"cloud_run_name": cloud_run_name, "backend_service_name": backend_service_name, "neg_name": neg_name}))
        
        neg_create_regional_cloud_run(region=region, neg_name=neg_name, cloud_run_service_name= cloud_run_name)
        entity['neg_name']=neg_name
        client.put(entity)
        backend_create_global(backend_service_name=backend_service_name, neg_name = neg_name, neg_region=region)
        entity['backend_service_name']=backend_service_name
        # entity['region']=region
        # entity["container_config"]=container_config
        entity["domain"]=domain
        client.put(entity)
        hostrule_add(domain=[domain], backend_service_name=backend_service_name, paths=["/test", "/dev", "/pre-prod"])

# Domain given and update
    elif domain_datastore!= 'None' and domain!=None:
        store_id=queryParams.get('store_id')
        region=str(json_data['region'])
        container_config=str(json_data['container_config'])
        preview_tagging_server_url=str(json_data['preview_tagging_server_url'])
        tagging_server_url = str(json_data['tagging_server-url'])
        
        domain = queryParams.get('domain')
        certificate_name = f'sst-{store_id}-certificate-{generate_random_string(10)}'
        print(certificate_name)
        list_domain, certis = domain_list(domain, certificate_name)
        print("domain_list",list_domain)
        ssl_create_managed(certificate_name=certificate_name, domains=list_domain)
        print("SSL certificate create successfully")
        entity['certificate_name']=certificate_name
        client.put(entity)
        # Function to check state of newly created certificate to be added
        https_proxy_attach_ssl_certificate(certificate_urls=certis)
        # Works till here Rev: test-backend-sst-lb-00018-lrx #


        # Latest revision additions Rev: test-backend-sst-lb-00019
        cloud_run_name = f"sst-{store_id}"
        backend_service_name = f"sst-{store_id}-be-{generate_random_string(10)}"
        neg_name = f"sst-{store_id}-neg-{generate_random_string(10)}"
        print(json.dumps({"cloud_run_name": cloud_run_name, "backend_service_name": backend_service_name, "neg_name": neg_name}))
        
        neg_create_regional_cloud_run(region=region, neg_name=neg_name, cloud_run_service_name= cloud_run_name)
        entity['neg_name']=neg_name
        client.put(entity)
        backend_create_global(backend_service_name=backend_service_name, neg_name = neg_name, neg_region=region)
        entity['backend_service_name']=backend_service_name
        # entity['region']=region
        # entity["container_config"]=container_config
        entity["domain"]=domain
        client.put(entity)
        hostrule_add(domain=[domain], backend_service_name=backend_service_name, paths=["/test", "/dev", "/pre-prod"])

    else:
        print("Domain not provided")
    
    return "Sucessfully updated"

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # Define the characters to include
    r1 = ''.join(random.choice(characters) for _ in range(length))
    random_string=r1.lower()
    return random_string
