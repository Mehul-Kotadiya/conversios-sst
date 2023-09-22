from ssl_1 import *
from lb import *

config = configparser.ConfigParser()
config.read('config.ini')

project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]

load_balancer = https_proxy_get()
certis = load_balancer.ssl_certificates

print(certis)


# exit()
length = 101
certi = {"managed":{"domains":[]}}
certi_list = []

for item in certis:
    certificate_domains = ssl_get_managed_domains(certificate_name)
    temp = {"name":certificate_name,"managed":{"domains":certificate_domains}}
    certi_list.append(temp)
    if len(certi["managed"]["domains"]) >= len(temp["managed"]["domains"]):
        certi = temp
    
    # sorted_data = sorted(data, key=lambda x: len(x.get('name', '')))


print(certi_list)
new_domain = "example.com"
certi["managed"]["domains"].append("example.com")


# new certificate to be created using ssl_create_managed with new name that currently doesn't exist.
# new certificate to be associated with load_balancer.
# once new certificate is in active state, old certificate to be deleted


# NEG: 
# Before backend is created, NetworkEndpointGroup to be created for Serverless Cloud Run (cloud run name+region in input)
# [https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.global_network_endpoint_groups.GlobalNetworkEndpointGroupsClient]

# Backend: 
# Create a method in lb.py to create a Backend Service for 
# [https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.backend_services.BackendServicesClient]
# Add Backend in LB
print(certi)