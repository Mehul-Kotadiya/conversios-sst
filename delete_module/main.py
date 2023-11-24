from google.cloud import compute_v1
import os
from google.cloud import pubsub_v1
import configparser
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from google.cloud import datastore
import time
import DomainList
project_id = 'server-side-tagging-392006'


datastore_client = datastore.Client()
store_id=[]
lb='test-lb-2'
proxy_name="-target-proxy"
my_list=[]
certi_fingerprint=[]
be_name=[]
neg_name=[]   
cd_certi_figer_print=[]
cd_final_certi_list=[]
patch_require_certi=[]
cd_certi_name_prefix= 'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/'
cd_full_url_certi=[]




#create FastAPI app
app = FastAPI(
    title="Backend Application to deploy and maintain multiple SSGTM",
    description= "Backend Application to deploy and maintain multiple SSGTM created via conversios frontend",
    version="1.0.0"
)


#add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
name=[]
final_cert_name=[]
final_status_check_cert=[]
length_check=[]
project = "server-side-tagging-392006"
subscription_name='server-side-tagging-topic-sub'
subscriber = pubsub_v1.SubscriberClient()

# task_key = client.key('server-side-tagging', store_id)
# task = client.get(task_key)

@app.get("/")
async def batch_function ():

    
    config = configparser.ConfigParser()
    config.read('config.ini')
    # ssl_delete(certificate_name='sst-10002-certificate-1700123575381')
    # exit()

    subscription_path = subscriber.subscription_path(project, subscription_name)

    num_messages = 1

    response = subscriber.pull(subscription=subscription_path, max_messages=num_messages)

    for received_message in response.received_messages:
        try:
            print(f"Received message: {received_message.message.data}")
            store_id.append(received_message.message.data.decode('utf-8'))
            # subscriber.acknowledge(
            # subscription=subscription_path,
            # ack_ids=[received_message.ack_id],
            # )        
        except Exception as e:
            print(f"Error processing or acknowledging the message: {e}")

    # exit()

    # ----------------------------- pubsub part
  
    # client = compute_v1.SslCertificatesClient()
    # ssl_certificates = client.list(project=project)
    # print('---------------------------------------------------')
    
    
   
    # json_formatted_data = []
    

    # for cert in ssl_certificates:

    #         certificate_data = {
    #             'name': cert.name,
    #             'status': cert.managed.status,
    #             'create_time': cert.creation_timestamp,
    #         }
    #         json_formatted_data.append(certificate_data)
    #         print(store_id[0])
    #         if str(store_id[0]) in cert.name: #set store id from datastore update part
    #              length_check.append(cert.name)
                 
            


    # print('check-length',len(length_check))
    # if len(length_check) == 2:
    #     #  print('now ready to run code')
    #     for cert in json_formatted_data:
    #         if str(store_id[0]) in cert['name']:
    #             name_data={
    #                 "name":cert['name'],
    #                 "status":cert['status'],
    #                 "create_time":cert['create_time']
    #             }
    #             print('**********')
                
                    
    #             name.append(name_data)
    #     # print(name)
    #     if name[0]['create_time'] < name[1]['create_time']:
    #         final_cert_name.append(name[0]['name'])
    #         final_status_check_cert.append(name[1]['name'])
    #     else:
    #         final_cert_name.append(name[1]['name'])
    #         final_status_check_cert.append(name[0]['name'])
    #     # print('--------')
    #     print('cert name',final_cert_name)
    #     print('status check',final_status_check_cert)
    certificate_99,latest_certificate,remaining_certificate = DomainList.domain_list()
    print('99 certi',certificate_99)
    print('latest_time',latest_certificate)
    print('remaining_certificate',remaining_certificate)
    delete_certi=remaining_certificate[0].split("/")[-1]
    patch_require_certi.append(certificate_99)
    patch_require_certi.append(latest_certificate)
    print('delete required',delete_certi)
    
    
    
    
    print('final certi status check',latest_certificate.split("/")[-1])    
    certi_status = get_ssl_certi(certificate_name=latest_certificate.split("/")[-1])
    print(certi_status)
    
    if certi_status == 'PROVISIONING':
        finger_print=https_proxy_get(load_balancer=lb)
        print('get proxy')
        patch_lb_front_end(load_balancer=lb,fingerprint=finger_print[0])
        print('update proxy')
        time.sleep(5)
        
        
        urlmap_get(lb=lb) #give static lb name
        print('url get and update path')
        time.sleep(5)
        get_backend_service()
        print('get backend')
        time.sleep(10)
        backend_delete(backend_service_name=be_name[0])
        time.sleep(10)
        print('delete backend')
        get_neg_list()
        time.sleep(10)
        print('get neg')

        neg_delete()
        time.sleep(10)
        print('delete neg')
        ssl_delete(certificate_name=delete_certi)
        print('All items deleted sucessfully')
        print(received_message)
        subscriber.acknowledge(
        subscription=subscription_path,
        ack_ids=[received_message.ack_id],
            )     





            # Deletion code start


    #         print('Our code work fine')
    else:
        print('The new certificate is not Active yet ')

    # else:
    #     print('Not required for delete operation because only one certificate is created')



    return {"message": "complete the scan"}



def get_ssl_certi(certificate_name:str):
    client = compute_v1.SslCertificatesClient()

    request = compute_v1.GetSslCertificateRequest(
    project=project,
    ssl_certificate=certificate_name,
)
    response = client.get(request=request)
    return response.managed.status




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    
    # batch_function()


# lb='test-lb-2'


# proxy_name="-target-proxy"
# my_list=[]

# certi_fingerprint=[]
# be_name=[]
# neg_name=[]    

#Loadbalancer get
def https_proxy_get(load_balancer: str):
    # print('proxy under',store_id[0])
    client = compute_v1.TargetHttpsProxiesClient()
    # task_key = datastore_client.key('server-side-tagging', str(store_id[0]))
    # task = datastore_client.get(task_key)
    # json_data={
    #     "certificate_name":task.get('certificate_name'),
    # }

    # certifinate_f_d=str(json_data['certificate_name'])
    new_lb = load_balancer
    tar_proxy=str(new_lb+proxy_name)
    # print("check",new_lb)
    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
    )
    # Make the request
    response = client.get(request=request)
    print('whole_response',response)
    # certis = response.ssl_certificates
    certi_fingerprint.append(response.fingerprint)
    # for cert in certis:
    #     if certifinate_f_d in cert:
    #         my_list.append(cert)
    # print(certis)
    return certi_fingerprint


def patch_lb_front_end(load_balancer:str,fingerprint:str):
    client = compute_v1.TargetHttpsProxiesClient()
    request_body={
        # "creation_timestamp": "2023-11-07T19:31:29.652-08:00",
        "fingerprint": fingerprint,
        # "id": 5701903430321618942,
        # "kind": "compute#targetHttpsProxy",
        # "name": "server-side-test-lb-target-proxy-2",
        # "quic_override": "NONE",
        "ssl_certificates" :patch_require_certi
        # [ 'https://www.googleapis.com/compute/v1/projects/tatvic-gcp-dev-team/global/sslCertificates/server-side-tagging-testing-certi2'],
        # "url_map": "https://www.googleapis.com/compute/v1/projects/tatvic-gcp-dev-team/global/urlMaps/server-side-test-lb"

    }
    new_lb = load_balancer   
    tar_proxy=str(new_lb+proxy_name)
    request = compute_v1.PatchTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
        target_https_proxy_resource=request_body    
    )
    response = client.patch(request=request)
    return response


def urlmap_get(lb: str):
    kind = 'server-side-tagging'
    parent_key=None
    print(str(store_id[0]),'------')
    custom_key = datastore_client.key(kind,str(store_id[0]),parent=parent_key)
    entity = datastore.Entity(key=custom_key)
    print('check urlmap updated?')


    task_key_updated = datastore_client.key('server-side-tagging-update-domain', str(store_id[0]))
    task_updated = datastore_client.get(task_key_updated)
    json_data_updated={
       "domain":task_updated.get('domain'), 
    }
    domain_updated = str(json_data_updated['domain'])
    task_key = datastore_client.key('server-side-tagging', str(store_id[0]))
    task = datastore_client.get(task_key)
    json_data={
        "certificate_name":task.get('certificate_name'),
        "store_id":task.get('store_id'),
        "region":task.get('region'),
        "preview_tagging_server_url":task.get('preview_tagging_server_url'),
        "container_config":task.get('container_config'),
        "tagging_server_url":task.get('tagging_server_url'),
        "domain":task.get('domain'),
        "neg_name":task.get('neg_name'),
        "backend_service_name":task.get('backend_service_name'),
    }

    certificate_name=str(json_data['certificate_name'])
    store_idd=str(json_data['store_id'])
    region=str(json_data['region'])
    container_config=str(json_data['container_config'])
    preview_tagging_server_url=str(json_data['preview_tagging_server_url'])
    tagging_server_url = str(json_data['tagging_server_url'])
    domain = str(json_data['domain'])
    neg_name = str(json_data['neg_name'])
    backend_service_name=str(json_data['backend_service_name'])




   
    client = compute_v1.UrlMapsClient()
    request = compute_v1.GetUrlMapRequest(
        project=project,  
        url_map=lb
    )
    response = client.get(request=request)
    # response.host_rules
    print((response.host_rules))
    print('--------')
    print(response.path_matchers)

    print("==========================")
    for i in response.host_rules:
        # print(i.hosts)
        if i.hosts[0] == domain:
            #domain not update in update part keep it old domain never update and then take from it 
            # print(i.path_matcher, type(i.path_matcher), sep=" >> ")

            for j in response.path_matchers:
                # j.name, type(j.name)
                if j.name == i.path_matcher:
                    response.path_matchers.remove(j)
            response.host_rules.remove(i)
    
    print(response.host_rules) 
    print('---------------')   
    print(response.path_matchers)
    # Patch request using response
    request = compute_v1.PatchUrlMapRequest(
        project=project,
        url_map=lb,
        url_map_resource = response
    )
    # Make the request
    response = client.patch(request=request)
    entity["store_id"]=store_idd
    entity["certificate_name"]=certificate_name
    entity["region"]=region
    entity["container_config"]=container_config
    entity["preview_tagging_server_url"]=preview_tagging_server_url
    entity["tagging_server_url"]=tagging_server_url
    entity["domain"]=domain_updated
    entity["neg_name"]=neg_name
    entity["backend_service_name"]=backend_service_name
    datastore_client.put(entity)
    # entity["store_id"]=store_id
    # entity["store_id"]=store_id


    # Handle the response
    print(response)
    return response





def get_backend_service():
    json_var={}
    item_list=[]
    item_list_final=[]
    client = compute_v1.BackendServicesClient()
    request = compute_v1.ListBackendServicesRequest(
        # backend_service=backend_service_name,
        project=project,
    )
    response = client.list(request=request)
    items = response.items
    for item in items:
        if str(store_id[0]) in item.name:
            item_list.append(item.name)
            item_list.append(item.creation_timestamp)
            json_var={
                "name":item.name,
                "create_time":item.creation_timestamp
            }
            item_list_final.append(json_var)
             # print(json_var)
            print('------------')
    print(item_list_final)
    # print(item_list_final[0]['name'])
    if item_list_final[0]['create_time'] < item_list_final[1]['create_time']:
        certname=(item_list_final[0]['name'])
    else:
        certname=(item_list_final[1]['name'])
    be_name.append(certname)
    print(be_name)
    return response


def backend_delete(backend_service_name:str):
    # Create a client
    client = compute_v1.BackendServicesClient()

    # Initialize request argument(s)
    request = compute_v1.DeleteBackendServiceRequest(
        backend_service=backend_service_name,
        project=project,
    )

    # Make the request
    response = client.delete(request=request)
    # Handle the response
    print(response)
    return response


def get_neg_list():
    # Create a client
    json_var={}
    item_list=[]
    item_list_final=[]
    client = compute_v1.RegionNetworkEndpointGroupsClient()
    task_key = datastore_client.key('server-side-tagging', str(store_id[0]))
    task = datastore_client.get(task_key)
    json_data={
        "region":task.get('region'),
    }

    region=str(json_data['region'])

    # Initialize request argument(s)
    request = compute_v1.ListRegionNetworkEndpointGroupsRequest(
        project=project,
        region=region,
    )

    # Make the request
    response = client.list(request=request)
    items = response.items
    for item in items:
        if str(store_id[0]) in item.name:
            item_list.append(item.name)
            item_list.append(item.creation_timestamp)
            json_var={
                "name":item.name,
                "create_time":item.creation_timestamp
            }
            item_list_final.append(json_var)
            print('------------')
    print(item_list_final)
 
    if item_list_final[0]['create_time'] < item_list_final[1]['create_time']:
        neg=(item_list_final[0]['name'])
    else:
        neg=(item_list_final[1]['name'])
    neg_name.append(neg)
    print(neg_name)
    return response


def neg_delete():
    # Create a client
    task_key = datastore_client.key('server-side-tagging', str(store_id[0]))
    task = datastore_client.get(task_key)
    json_data={
        "region":task.get('region'),
    }

    region=str(json_data['region'])
    

    # #region="us-central1" #get from datastore
    client = compute_v1.RegionNetworkEndpointGroupsClient()

    # Initialize request argument(s)
    request = compute_v1.DeleteRegionNetworkEndpointGroupRequest(

        network_endpoint_group=neg_name[0],
        # network_endpoint_group='sst-13241-neg-1700030259258',
        project=project,
        region=region
        )
    response = client.delete(request=request)
    print(response)
# neg_delete()


def ssl_delete(certificate_name):
    client = compute_v1.SslCertificatesClient()
    print(1)

    request = compute_v1.DeleteSslCertificateRequest(
        project= project,
        ssl_certificate= certificate_name
    )
    print(2)
    try:
        # Make the delete request
        response = client.delete(request=request)
        print(response)
        print('deleted succesfully')
    except Exception as e:
        print(f"An error occurred: {e}")





@app.get("/create-delete")

def create_delete_batch():

    full_url_certi = []
    certificate_99,latest_certificate,remaining_certificate = DomainList.domain_list()
    full_url_certi.append(certificate_99)
    full_url_certi.append(latest_certificate)
    certi_status = get_ssl_certi(latest_certificate.split("/")[-1])
    print(certi_status)
    try:
        if certi_status == 'PROVISIONING' :
        
            finger_print=create_delete_https_proxy_get()
            create_delete_patch_lb_front_end(certilist=full_url_certi,fingerprint=finger_print[0])     
            time.sleep(10)
            for i in remaining_certificate:
                print(i)
                certificate_name=i.split("/")[-1]
                create_delete_ssl_delete(certificate_name)
                print('delete certi',remaining_certificate)

        else:
            print('There is no new certificate is create')
    except Exception as e:
        print(e)





    return 'Function run well'

def create_delete_https_proxy_get():
    print('i am proxy get under')

    client = compute_v1.TargetHttpsProxiesClient()
    
    new_lb = lb
    tar_proxy=str(new_lb+proxy_name)
    # print("check",new_lb)
    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
    )
    # Make the request
    response = client.get(request=request)
    # print('whole_response',response)
    certis = response.ssl_certificates
    cd_certi_figer_print.append(response.fingerprint)
   
    return cd_certi_figer_print


def create_delete_patch_lb_front_end(certilist:list,fingerprint:str):
    print('i am under patch function')
    client = compute_v1.TargetHttpsProxiesClient()
    request_body={
        # "creation_timestamp": "2023-11-07T19:31:29.652-08:00",
        "fingerprint": fingerprint,
        # "id": 5701903430321618942,
        # "kind": "compute#targetHttpsProxy",
        # "name": "server-side-test-lb-target-proxy-2",
        # "quic_override": "NONE",
        "ssl_certificates" :certilist
        # [ 'https://www.googleapis.com/compute/v1/projects/tatvic-gcp-dev-team/global/sslCertificates/server-side-tagging-testing-certi2'],
        # "url_map": "https://www.googleapis.com/compute/v1/projects/tatvic-gcp-dev-team/global/urlMaps/server-side-test-lb"

    }
    new_lb =lb   
    tar_proxy=str(new_lb+proxy_name)
    request = compute_v1.PatchTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
        target_https_proxy_resource=request_body    
    )
    response = client.patch(request=request)
    print(response)
    return response

def create_delete_ssl_delete(certificate_name):
    client = compute_v1.SslCertificatesClient()
    

    request = compute_v1.DeleteSslCertificateRequest(
        project= project,
        ssl_certificate= certificate_name
    )
   
    try:
        # Make the delete request
        response = client.delete(request=request)
        print(response)
        print('certificate '+certificate_name +' deleted succesfully')
    except Exception as e:
        print(f"An error occurred: {e}")