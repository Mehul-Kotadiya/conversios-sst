from google.cloud import compute_v1
from ssl_1 import *
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]

client = compute_v1.TargetHttpsProxiesClient()


def https_proxy_get():
    new_lb = lb + "-target-proxy-2"

    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=new_lb,
    )

    # Make the request
    response = client.get(request=request)
    return response


def https_proxy_list():
    # Initialize request argument(s)
    request = compute_v1.ListTargetHttpsProxiesRequest(
        project=project,
    )

    # Make the request
    page_result = client.list(request=request)

    # Handle the response
    for response in page_result:
        print(response)

def https_proxy_attach_ssl_certificate():

    # compute_service = build('compute', 'v1', credentials=credentials)
    # client = compute_v1.TargetHttpsProxiesClient()


    project_id = 'tatvic-gcp-dev-team'
    load_balancer_name = 'test-lb-target-proxy'
    new_certi_name = 'test-ssl-3'
    old_certi_name = "test-ssl-2"
    newer_certi_name = "test-ssl-1"

    new_certificate_url = 'https://www.googleapis.com/compute/v1/projects/{}/global/sslCertificates/{}'.format(project_id,new_certi_name)
    old_certificate_url = 'https://www.googleapis.com/compute/v1/projects/{}/global/sslCertificates/{}'.format(project_id,old_certi_name)
    newer_certi_name = 'https://www.googleapis.com/compute/v1/projects/{}/global/sslCertificates/{}'.format(project_id,newer_certi_name)

    request_body = {
        'ssl_certificates': [new_certificate_url, old_certificate_url, newer_certi_name]
    }

    # Initialize request argument(s)
    request = compute_v1.SetSslCertificatesTargetHttpsProxyRequest(
        project= project_id,
        target_https_proxy= load_balancer_name,
        target_https_proxies_set_ssl_certificates_request_resource = request_body
    )

    # Make the request
    response = client.set_ssl_certificates(request=request)

    # response = client.TargetHttpsProxy().setSslCertificates(
    #     project=project_id,
    #     targetHttpsProxy=load_balancer_name,
    #     body=request_body
    # ).execute()

    print("Certificate updated:", response)

load_balancer = https_proxy_get()
print(load_balancer)
# for certi in load_balancer.ssl_certificates:
#     domains = ssl_get_managed_domains(certi)
#     print(domains)

# x = https_proxy_attach_ssl_certificate()
# print(x)
