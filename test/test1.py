# from DomainList import  domain_list
import time
from google.cloud import compute_v1
import configparser
import datetime


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]
proxy_name="-target-proxy"
client = compute_v1.TargetHttpsProxiesClient()

def https_proxy_get(load_balancer: str):
    
    new_lb = load_balancer
    tar_proxy=str(new_lb+proxy_name)
    # print("check",new_lb)
    request = compute_v1.GetTargetHttpsProxyRequest(
        project=project,
        target_https_proxy=tar_proxy
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
    return response.managed.domains

def ssl_get_latest_domains_(certificate_name):
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

def domain_list(new_domain: str,certificate_name: str):
    # print(lb)
    certificates = https_proxy_get(load_balancer=lb)
    
    dic1 = {}
    latest_certificate = None
    latest_timestamp = None

    for i in certificates:
          print("start")
          max_timestamp,domains, = ssl_get_latest_domains_(i)
          dic1[i]= []
          dic1[i].append(max_timestamp)
          dic1[i].append(domains)

    for certificate, data in dic1.items():
        timestamp = data[0]
        if latest_timestamp is None or timestamp > latest_timestamp:
            latest_certificate = certificate
            latest_timestamp = timestamp

# Merge domains of all previous certificates into the latest one

    if latest_certificate:
        domains_to_merge = []
        for certificate, data in dic1.items():
            if certificate != latest_certificate:
                domains_to_merge.extend(data[1])

        dic1[latest_certificate][1].extend(domains_to_merge)
        dic1[latest_certificate][1] = list(set(dic1[latest_certificate][1]))

    new_certificate_domains= dic1[latest_certificate][1]
    certificates=[]
    certificate = list(dic1.keys())
    new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
    certificates.append(new_certificate)

    return new_certificate_domains, certificates


timestamp1= round(time.time()*1000)
certificate_name = f'sst-certificate-{timestamp1}'
new_certificate_domains, certificates = domain_list("deep.com",certificate_name)
# print(new_certificate_domains, certificates )

# # Read input data from a JSON file
# with open('/home/yash/Desktop/sony_iam.json', 'r') as input_file:
#     items = json.load(input_file)

# # Serialize each item as JSON and join with newline characters
# with open('/home/yash/Desktop/sony_iam_output.json', 'w') as output_file:
#     for i in items:
#         # Serialize the current item as JSON and write it as a separate line
#         json_string = json.dumps(i)
#         output_file.write(json_string+"\n")
    