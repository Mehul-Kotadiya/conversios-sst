from google.cloud import compute_v1
import os
from google.cloud import pubsub_v1
import configparser
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from google.cloud import datastore
import time
import DomainList
import logging
project_id = 'server-side-tagging-392006'

# set up the Google Cloud Logging python client library
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging()

# logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s',filemode='w')
# logging = logging.getlogging()

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
# subscriber = pubsub_v1.SubscriberClient()

# @app.get("/update_delete")
# async def batch_function ():
#     print('hi')
    
#     config = configparser.ConfigParser()
#     config.read('config.ini')

#     subscription_path = subscriber.subscription_path(project, subscription_name)

#     num_messages = 1

#     response = subscriber.pull(subscription=subscription_path, max_messages=num_messages)
#     print(response.received_messages)

#     for received_message in response.received_messages:
#         try:
#             print(received_message)
#             print(f"Received message: {received_message.message.data}")
#             store_id.append(received_message.message.data.decode('utf-8'))
            
#             # print(ack)
#             # exit()
#             # subscriber.acknowledge(
#             # subscription=subscrack=received_message.ack_idiption_path,
#             # ack_ids=[received_message.ack_id],
#             # )          
#             certificate_99,latest_certificate,remaining_certificate = DomainList.domain_list()
#             print('99 certi',certificate_99)
#             print('latest_time',latest_certificate)
#             print('remaining_certificate',remaining_certificate)
#             if len(remaining_certificate)==0:

#                 # delete_certi=remaining_certificate[0].split("/")[-1]
#                 patch_require_certi.append(certificate_99)
#                 patch_require_certi.append(latest_certificate)
#                 # print('delete required',delete_certi)
                    
                
#                 print('final certi status check',latest_certificate.split("/")[-1])    
#                 certi_status = get_ssl_certi(certificate_name=latest_certificate.split("/")[-1])
#                 print(certi_status)
                
#                 if certi_status == 'Active':
#                     # finger_print=https_proxy_get(load_balancer=lb)
#                     print('get proxy part skip')
#                     # patch_lb_front_end(load_balancer=lb,fingerprint=finger_print[0])
#                     print('update proxy part skip')
#                     # time.sleep(5)
                    
                    
#                     urlmap_get(lb=lb) #give static lb name
#                     print('url get and update path')
#                     time.sleep(5)
#                     get_backend_service()
#                     print('get backend')
#                     time.sleep(10)
#                     backend_delete(backend_service_name=be_name[0])
#                     time.sleep(10)
#                     print('delete backend')
#                     get_neg_list()
#                     time.sleep(10)
#                     print('get neg')

#                     neg_delete()
#                     time.sleep(10)
#                     print('delete neg')
#                     # ssl_delete(certificate_name=delete_certi)
#                     print('delete certi part skip')
#                     print('All items deleted sucessfully')
#                     print("pointer",received_message)
#                     # print("mid",received_message['message']['message_id'])
#                     # print("mid2",received_message.message.message_id)
#                     ack=received_message.ack_id
#                     res=subscriber.acknowledge(
#                     subscription=subscription_path,
#                     ack_ids=[ack],
#                         )     
#                     print('pubsub res',res)
#                 else:
#                     print('The new certificate is not Active yet ')

#                 content = {"message": "complete the scan"}
#                 return JSONResponse(content=content, status_code=200)
#             else:
#                 print('no deleteion required')
#         except Exception as e:
#             print(f"Error processing or acknowledging the message: {e}")


''' Delete the perivous certificate'''

@app.get("/create_delete")
async def create_delete_batch(request: Request):
    print('start create delete')
    logging.info('Logging is sucessfully set')
    # certi_create()
    # exit()

    full_url_certi = []
    certificate_99,latest_certificate,remaining_certificate = DomainList.domain_list()
    print('domain list complete')
    logging.info('certificate fetch is sucessfully')
    # print('certificate_99',certificate_99)
    # print('latest_certificate',latest_certificate)
    # print('remaining_certificate',remaining_certificate)
    if len(remaining_certificate) != 0:
        full_url_certi.append(certificate_99)
        full_url_certi.append(latest_certificate)
        certi_status = get_ssl_certi(latest_certificate.split("/")[-1])
        print('ssl certi complete')
        logging.info('get ssl certi end')
        # print(certi_status)
        try:
            if certi_status == 'PROVISIONING' :
                logging.info('under try')
                
            
                finger_print=create_delete_https_proxy_get()
                logging.info('fingerprint end')

              
                #Patch request on Loadbalancer with updated certificate
                create_delete_patch_lb_front_end(certilist=full_url_certi,fingerprint=finger_print[0])
                logging.info('Patch request is sucessfully set')
                print('Patch request is sucessfully set')
                   
                time.sleep(10)
                for i in remaining_certificate:
                    logging.info('Under delete request')
                    print('Under delete request')
                    print('delete required certi',remaining_certificate)
                    certificate_name=i.split("/")[-1]
                    # logging.info("certificate required to delete",certificate_name)
                    print('delete required certi list',certificate_name)
                   
                    #Delete non-required certificate
                    time.sleep(10)
                    create_delete_ssl_delete(certificate_name)
                    
                    


            else:
                return 'There is no new certificate is create'
        except Exception as e:
            print(e)
    else:
        print('There is no required delete operation')


    return 'Function run Successfully-'

def create_delete_https_proxy_get():
    client = compute_v1.TargetHttpsProxiesClient()
    new_lb = lb
    tar_proxy=str(new_lb+proxy_name)
    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
    )
    # Make the request
    response = client.get(request=request)
    certis = response.ssl_certificates
    cd_certi_figer_print.append(response.fingerprint)
   
    return cd_certi_figer_print

def create_delete_patch_lb_front_end(certilist:list,fingerprint:str):
    logging.info("under patch function")

    
    client = compute_v1.TargetHttpsProxiesClient()
    request_body={
        "fingerprint": fingerprint,
        "ssl_certificates" :certilist
    }
    logging.info('requestbody created')
    new_lb =lb   
    tar_proxy=str(new_lb+proxy_name)
    # print('under patch lb before request',certilist)
    logging.info('request before')
    
    request = compute_v1.PatchTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
        target_https_proxy_resource=request_body    
    )
    logging.info('response before')
    response = client.patch(request=request)
    logging.info("patch function end")
   
    return response

def create_delete_ssl_delete(certificate_name):
    logging.info("under delete certi function")
    client = compute_v1.SslCertificatesClient()
    request = compute_v1.DeleteSslCertificateRequest(
        project= project,
        ssl_certificate= certificate_name
    )
   
    try:
        # Make the delete request
        response = client.delete(request=request)
        logging.info("under delete certi function try")
        print('certificate '+certificate_name +' deleted succesfully')
    except Exception as e:
        logging.info("error occures",e)
        print(f"An error occurred: {e}")

    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8080, reload=True)

def get_ssl_certi(certificate_name:str):
    client = compute_v1.SslCertificatesClient()

    request = compute_v1.GetSslCertificateRequest(
    project=project,
    ssl_certificate=certificate_name,
)
    response = client.get(request=request)
    return response.managed.status


# def certi_create():
    domain_listt_dupli=[
    "exampvcbnle1.com", "testdocvbnmain.net", "dummybvnwebsite.org", "samplvcbepage.com", "mocksite.net",
    "placevcbnholder.org", "trythisdomain.com", "fauxwebsite.net", "tempdbvnomain.org", "mytestsite.com",
    "pretendpage.net", "fakedom465ain.org", "trialwebsite.com", "imitationnet.net", "demobvnorg.org",
    "playdbvnomain.com", "fictiondfgalpage.net", "sandbox.org", "testdummy.com", "faketestsite.net",
    "notrbvneal.org", "mimicdomain.com", "trialsite.net", "dummywebpage.org", "fauxsite.com",
    "exagfbnmple.net", "prefgbtendweb.org", "placeholfghderpage.com", "test1net.net", "tempwebsite.org",
    "trydomain.com", "sampleorg.net", "mockdgbfhummy.org", "mywebsgbvhite.com", "notrealnet.net",
    "imitationpage.com", "demoorg.net", "playdomain.org", "pretecvbndnet.com", "sandboxsite.net",
    "testdummy.org", "faketest.com", "notrealpage.net", "mimiccvbdomain.org", "trialsite.com",
    "dummyweb.net", "fauxsite.org", "examplepage.com", "trywebsite.net", "placeholder.net",
    "testdomain.org", "fakedummy.com", "samplewebsite.net", "tempdocvbnmain2.org", "mytestsite.com",
    "pretendpage.net", "fak3etest.org", "imitation.com", "trialsite.net", "dummywebpage.org",
    "sandboxsite.com", "testdummy.net", "fauxdomain.org", "examplewebsite.com", "notreal.net",
    "mimi4cpage.org", "playdomain.com", "pret4endweb.net", "tempd1omain1.org", "tryth8isdomain.com",
    "samplepag6e.net", "mocksdfgs5ite.org", "placeholder.com", "fakedomain.net", "trialwebsite.org",
    "imitationnet.com", "demoorg.net", "playdomain.org", "notrealwebsite.com", "mimicdomain.net",
    "trialsite.org", "dummywebpag4e.com", "fauxs3ite.net", "exa7mple.org", "pretend8net.com",
    "placeholderpage.net", "testnet.org", "tempwebsite.com", "tr1ydomain.net", "sampleorg.org",
    "mockdummy.com", "mywebsite.net", "notrealne1t.org", "fakedoma7in.net", "imitationpage.net",
    "demoorg.com", "playdomain.net", "preten6dnet.org","yrfdtguh.com","dtfyguhji.com","gvftr5768y.com","jkbhgfch987.com","jkhvtfguy675.com","wertyu.net","765rtyujhgftyu.org"
]
    unique_list = list(set(domain_listt_dupli))
    
    certi_name = 'test-certi-99-test'
    client = compute_v1.SslCertificatesClient()

    ssl_certificate = compute_v1.SslCertificate(
        name=certi_name,
        managed=compute_v1.SslCertificateManagedSslCertificate(
            domains=unique_list
        ),
        type="MANAGED"
    )
    request = compute_v1.InsertSslCertificateRequest(
        project=project,
        ssl_certificate_resource=ssl_certificate
    )

    response = client.insert(request=request)
    response = response.result()
    return response