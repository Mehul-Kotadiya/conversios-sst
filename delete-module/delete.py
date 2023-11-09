from google.cloud import compute_v1
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]
proxy_name="-target-proxy"


client = compute_v1.SslCertificatesClient()
ssl_certificates = client.list(project=project)
my_domain = 'newdomain2.com'
json_formatted_data = []
certi_status=[]

for cert in ssl_certificates:
    name = cert.name
    status = cert.managed.status
    domains = cert.managed.domains

    certificate_data = {
        'name': name,
        'domain': domains,
        'status': status,
    }

    json_formatted_data.append(certificate_data)
    print(json_formatted_data)

# for i in json_formatted_data:
#     if 'example.com' in i['domain']:
#         certi_status.append(i['status'])

# for cert in certi_status:
#     if cert=='Provisioning':
#         print('Active')
#     else:
#         print(cert)