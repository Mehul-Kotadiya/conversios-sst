from google.cloud import compute_v1
from lib.SSL import *
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
project_id = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]

client = compute_v1.TargetHttpsProxiesClient()


def https_proxy_get(load_balancer: str):
    new_lb = load_balancer

    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=new_lb,
    )

    # Make the request
    response = client.get(request=request)
    certis = response.ssl_certificates
    return certis


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

def https_proxy_attach_ssl_certificate(certis,new_certificate_name):

    # compute_service = build('compute', 'v1', credentials=credentials)
    # client = compute_v1.TargetHttpsProxiesClient()

    # load_balancer_name = 'test-lb-target-proxy'
    certificate_urls=[]
    for item in certis:
        certificate_urls.append(f'https://www.googleapis.com/compute/v1/projects/{project_id}/global/sslCertificates/{item}')

    new_certificate_url=f'https://www.googleapis.com/compute/v1/projects/{project_id}/global/sslCertificates/{new_certificate_name}'

    certificate_urls.append(new_certificate_url)
    

    request_body = {
        'ssl_certificates': certificate_urls
    }

    # Initialize request argument(s)
    request = compute_v1.SetSslCertificatesTargetHttpsProxyRequest(
        project= project_id,
        target_https_proxy= lb,
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
