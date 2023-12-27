import configparser
import time 
from google.cloud import compute_v1
import logging

config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]
proxy_name="-target-proxy"

#===============================================================================
def https_proxy_get(load_balancer: str):
    client = compute_v1.TargetHttpsProxiesClient()
    new_lb = load_balancer
    tar_proxy=str(new_lb+proxy_name)
    # print("check",new_lb)
    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy,
    )
    # Make the request
    response = client.get(request=request)
    # print('re',response)
    certis = response.ssl_certificates
    return certis

def ssl_get_managed_domains(certificate_name):
    client = compute_v1.SslCertificatesClient()

    # Initialize request argument(s)
    if certificate_name.startswith("https://www.googleapis.com/compute/v1/projects/"):
        certificate_name = certificate_name.split("/")[-1]

    request = compute_v1.GetSslCertificateRequest(
        project=project,
        ssl_certificate=certificate_name,
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    return response.creation_timestamp, response.managed.domains



def domain_list():
    # print(lb)
    logging.info('i am under domain list function')
    all_certificates = https_proxy_get(load_balancer=lb)
    # print('all',all_certificates)
    logging.info('proxy get function end')
    
    dic1 = {}
    latest_certificate = None
    latest_timestamp = None

    for i in all_certificates:
        #   print("start")
          max_timestamp,domains, = ssl_get_managed_domains(i)
          logging.info('sst managed get domains function end')
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

    certificate_99 = None
    for certificate, data in dic1.items():
        each_cnt_domain = len(data[1])
        if  each_cnt_domain == 99:
            certificate_99 = certificate
        
    # print('99',certificate_99)
    remaining_certificate = []
    remaining_certificate = list(dic1.keys())
    # print('remaining_certificate',remaining_certificate)
    if certificate_99 != None:
        remaining_certificate.remove(certificate_99)

    if latest_certificate != None:
        remaining_certificate.remove(latest_certificate)
    # print('done')
    logging.info('domain list function end')
    
    return certificate_99, latest_certificate,remaining_certificate


