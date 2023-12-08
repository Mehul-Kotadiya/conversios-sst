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
# from google.cloud import pubsub_v1

import random
import string
import time
# project_id="server-side-tagging-392006"


router = APIRouter()
client = datastore.Client()


project_id = 'server-side-tagging-392006'
topic_name='server-side-tagging-topic'
certi_status_check=[]

@router.post('/datastore_entry')
async def datastore_entry(request: Request):
    timestamp1= round(time.time()*1000)
    payload_bytes = await request.body()
    print(payload_bytes)
    payload_str = payload_bytes.decode("utf-8")
    queryParams = json.loads(payload_str)
    print(queryParams)

    store_id = queryParams.get('store_id')
    region = queryParams.get('region')
    domain = queryParams.get('domain')
    container_config = queryParams.get('container_config')
    print('region',region)

    if region != None:
        print('This is create request')
        kind='create_request_queue'
        key = client.key(kind,str(store_id))
        entity=datastore.Entity(key=key)
        entity["name"]=store_id
        entity['region']=region
        entity['domain']=domain
        entity['container_config']=container_config
        entity['entry_time']=timestamp1
        client.put(entity)


    else:
        print('This is update request')

        update_kind='update_request_queue'
        update_key = client.key(update_kind,str(store_id))
        updated_entity=datastore.Entity(key=update_key)
        updated_entity["name"]=store_id
        updated_entity['domain']=domain
        updated_entity['container_config']=container_config
        updated_entity['entry_time']=timestamp1
        client.put(updated_entity)
        


    return 'function sucessfully run'










@router.get('/create')

async def sst_create(request: Request):
    timestamp1= round(time.time()*1000)

    
    certi_status=latest_certi_find()
    print(certi_status)
    if certi_status == 'PROVISIONING':
    # payload_bytes = await request.body()
    # print(payload_bytes)
    # payload_str = payload_bytes.decode("utf-8")
    # queryParams = json.loads(payload_str)
    # print(queryParams)
        cr_kind = 'create_request_queue'
        cr_data=client.query(kind=cr_kind)
        cr_entities = list(cr_data.fetch())
        entry_list=[]
        for e in cr_entities:
        # print(time.append(e['create_at']))
            min_time={
                'time':e['entry_time'],
                'store_id':e['name'],
                'region':e['region'],
                'container_config':e['container_config'],
                'domain':e['domain'],

            }
        entry_list.append(min_time)
        if entry_list != []:

            min_time_entry = min(entry_list, key=lambda x: x['time'])
            if min_time_entry['store_id'] != 'null' and min_time_entry['store_id'] != '' and min_time_entry['store_id'] != None:
                store_id=min_time_entry['store_id']
                region=min_time_entry['region']
                domain=min_time_entry['domain']
                container_config=min_time_entry['container_config']
            # else:
            #     print('its dummy entry')

            #datastore part
                kind = 'server-side-tagging'
                # parent_key=None
                custom_key = client.key(kind,str(store_id))
                entity = datastore.Entity(key=custom_key)
                print("name", type(store_id))
                print("region", type(region))
                print("container_config", type(container_config))



                # entity["name"]=store_id
                # entity['region']=region
                # entity['domain']=domain
                # entity['container_config']=container_config
                # client.put(entity)
                

                print("name", store_id)
                print("region", region)
                print("container_config", container_config)
               

                preview_server_url, preview_name = await create_service_preview_tagging(store_id, region, container_config)
                sample_set_iam_policy(preview_name)
                print('preview-created')
                result1, tagging_name, details = await create_service_tagging(store_id, region, container_config, preview_server_url)
                sample_set_iam_policy(tagging_name)
                print('all-created')
                delete_entry = client.key(cr_kind,store_id)
                client.delete(delete_entry)

                entity["name"]=store_id
                entity['region']=region
                entity['domain']=domain
                entity['container_config']=container_config
                entity['preview_tagging_server_url']=preview_server_url
                entity['tagging_server_url']=result1
                client.put(entity)
            

            

                if domain!= None:
                    certificate_name = f'sst-{store_id}-certificate-{timestamp1}'
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
                    backend_service_name = f"sst-{store_id}-be-{timestamp1}"
                    neg_name = f"sst-{store_id}-neg-{timestamp1}"
                    print(json.dumps({"cloud_run_name": cloud_run_name, "backend_service_name": backend_service_name, "neg_name": neg_name}))
                    
                    neg_create_regional_cloud_run(region=region, neg_name=neg_name, cloud_run_service_name= cloud_run_name)
                    entity['neg_name']=neg_name
                    client.put(entity)
                    backend_create_global(backend_service_name=backend_service_name, neg_name = neg_name, neg_region=region)
                    entity['backend_service_name']=backend_service_name
                    client.put(entity)
                    hostrule_add(domain=[domain], backend_service_name=backend_service_name, paths=["/test", "/dev", "/pre-prod"])
                else:
                    print('Domain not provided')

            else:
                print('Store id is Null')

        else:
            print('Datastore in to create request')

    else:
        print('Request is under process')
            

    return {"Payload Details": details}

@router.get("/my-update")
async def update(request:Request):
    timestamp1= round(time.time()*1000)


    # payload_bytes = await request.body()
    # print(payload_bytes)
    # payload_str = payload_bytes.decode("utf-8")
    # queryParams = json.loads(payload_str)
    # print(queryParams)

    certi_status=latest_certi_find()
    print(certi_status)
    if certi_status == 'PROVISIONING':
        up_kind = 'update_request_queue'
        up_data=client.query(kind=up_kind)
        up_entities = list(up_data.fetch())
        entry_list=[]
        for e in up_entities:
        # print(time.append(e['create_at']))
            min_time={
                'time':e['entry_time'],
                'store_id':e['name'],
                'container_config':e['container_config'],
                'domain':e['domain'],

            }
        entry_list.append(min_time)

        

        if entry_list != []:

            min_time_entry = min(entry_list, key=lambda x: x['time'])
            if min_time_entry['store_id'] != 'null' and min_time_entry['store_id'] != '' and min_time_entry['store_id'] != None:
            
                print(min_time_entry)
                store_id=min_time_entry['store_id']
                domain=min_time_entry['domain']
                container_config=min_time_entry['container_config']
           


        # else:
        #     print('its blank')


        # store_id = queryParams.get('store_id')
        # container_config = queryParams.get('container_config')
        # domain = queryParams.get('domain')
        # print('today_domain_check',domain)







                print('its run',store_id)
                print(container_config)
                print(domain)

                
                




                kind = 'server-side-tagging'
                # parent_key=None
                custom_key = client.key(kind,str(store_id))
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
                    print('Container config given and update')
                    timestamp1= round(time.time()*1000)
                    store_id=min_time_entry['store_id']
                    # #region=str(json_data['region'])
                    domain=str(json_data['domain'])
                    # container_config=str(json_data['container_config'])
                    preview_tagging_server_url=str(json_data['preview_tagging_server_url'])
                    tagging_server_url = str(json_data['tagging_server_url'])
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

                    delete_entry = client.key(up_kind,store_id)
                    client.delete(delete_entry)
                else:
                    print("Container config not provided")


                # print(operation.result)
                print('ds_domain',domain_datastore)

            # Domain not given and update
                if domain_datastore == 'None' and domain != None:
                    print('Domain not given and update')
                    timestamp1= round(time.time()*1000)
                    store_id=min_time_entry['store_id']
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
                    domain=min_time_entry['domain']
                    print('ud',domain)

                    


                    certificate_name = f'sst-{store_id}-certificate-{timestamp1}'
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
                    backend_service_name = f"sst-{store_id}-be-{timestamp1}"
                    neg_name = f"sst-{store_id}-neg-{timestamp1}"
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
                    delete_entry = client.key(up_kind,store_id)
                    client.delete(delete_entry)

            # Domain given and update
                elif domain_datastore!= 'None' and domain!=None:
                    timestamp1= round(time.time()*1000)

                    print('I am in Domain given and update section')
                    store_id=min_time_entry['store_id']
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


                    region=str(json_data['region'])
                    container_config=str(json_data['container_config'])
                    preview_tagging_server_url=str(json_data['preview_tagging_server_url'])
                    tagging_server_url = str(json_data['tagging_server_url'])
                    domain=min_time_entry['domain']
                    domain_old = str(json_data['domain'])
                    neg_name=str(json_data['neg_name'])
                    backend_service_name=str(json_data['backend_service_name'])
                    # certificate_name=str(json_data['certificate_name'])
                    print('old domain',domain_old)
                    print('new domain',domain)

                    #datastore use for update domain
                    kind_update = 'server-side-tagging-update-domain'
                    parent_key=None
                    custom_key_update = client.key(kind_update,str(store_id),parent=parent_key)
                    entity_update = datastore.Entity(key=custom_key_update)

                    certificate_name = f'sst-{store_id}-certificate-{timestamp1}'
                    print(certificate_name)
                    list_domain, certis = domain_list(domain, certificate_name)
                    print("domain_list",list_domain)
                    for d in list_domain:
                        if domain_old ==d:
                            list_domain.remove(d)
                        else:
                            print('This is not update request')
                    # list_domain.append(domain)
                    print('final domain list',list_domain)
                    ssl_create_managed(certificate_name=certificate_name, domains=list_domain)
                    print("SSL certificate create successfully")
                    entity['certificate_name']=certificate_name
                    client.put(entity)
                    # Function to check state of newly created certificate to be added
                    https_proxy_attach_ssl_certificate(certificate_urls=certis)
                    # Works till here Rev: test-backend-sst-lb-00018-lrx #


                    # Latest revision additions Rev: test-backend-sst-lb-00019
                    # cloud_run_name = f"sst-{store_id}"
                    # backend_service_name = f"sst-{store_id}-be-{timestamp1}"
                    # neg_name = f"sst-{store_id}-neg-{timestamp1}"
                    # print(json.dumps({"cloud_run_name": cloud_run_name, "backend_service_name": backend_service_name, "neg_name": neg_name}))
                    
                    # neg_create_regional_cloud_run(region=region, neg_name=neg_name, cloud_run_service_name= cloud_run_name)
                    # entity['neg_name']=neg_name
                    # client.put(entity)
                    # backend_create_global(backend_service_name=backend_service_name, neg_name = neg_name, neg_region=region)
                    update_routing_rule(new_host=domain,old_host=domain_old)
                    entity['neg_name']=neg_name
                    entity['backend_service_name']=backend_service_name
                    entity['store_id']=store_id
                    entity['region']=region
                    entity["container_config"]=container_config
                    entity["preview_tagging_server_url"]=preview_tagging_server_url
                    entity["tagging_server_url"]=tagging_server_url
                    entity["domain"]=domain
                    client.put(entity)
                    entity_update['domain']=domain
                    client.put(entity_update)
                    # hostrule_add(domain=[domain], backend_service_name=backend_service_name, paths=["/test", "/dev", "/pre-prod"])
                    # publisher = pubsub_v1.PublisherClient()
                    # topic_path = publisher.topic_path(project_id,topic_name)

                    # message_data=store_id
                    # future = publisher.publish(topic_path, data=message_data.encode("utf-8"))
                    # future.result()

                    # print("Published message to Pub/Sub:", message_data)
                    delete_entry = client.key(up_kind,store_id)
                    client.delete(delete_entry)
                

                else:
                    print("Domain not provided")

            else:
                print('Store id is null')

        else:
            print('Empty List')
    
    else:
        print('Request is under process')    
    return "Sucessfully updated"


# def generate_random_string(length):
#     characters = string.ascii_letters + string.digits  # Define the characters to include
#     r1 = ''.join(random.choice(characters) for _ in range(length))
#     random_string=r1.lower()
#     return random_string


def latest_certi_find():
    all_certificates = https_proxy_get(load_balancer=lb)
    print('https proxy get sucessfully run')
    
    dic1 = {}
    latest_certificate = None
    latest_timestamp = None

    for i in all_certificates:
        #   print("start")
          max_timestamp,domains, = ssl_get_managed_domains(i)
          print('all atteched domain found')
          dic1[i]= []
          dic1[i].append(max_timestamp)
          dic1[i].append(domains)

    cnt_domain=0
    for certificate, data in dic1.items():
        timestamp = data[0]
        if latest_timestamp is None or timestamp > latest_timestamp:
            latest_certificate = certificate
            latest_timestamp = timestamp
            cnt_domain = len(data[1])

# Merge domains of all previous certificates into the latest one

    # print("latest",latest_certificate)
    certi_status_check.append(latest_certificate.split("/")[-1])
    certi_status =get_ssl_certi(certi_status_check[0])
    return certi_status

def get_ssl_certi(certificate_name:str):
    client = compute_v1.SslCertificatesClient()

    request = compute_v1.GetSslCertificateRequest(
    project=project,
    ssl_certificate=certificate_name,
)
    response = client.get(request=request)
    return response.managed.status