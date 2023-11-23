import configparser
from lib.LB import *
from lib.SSL import *
import time 

config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]


# def domain_list(new_domain: str,certificate_name: str):
#     print(lb)
#     certificates = https_proxy_get(load_balancer=lb)
#     # certi_list = []
#     # smallest_certificate = None
#     smallest_domain_count = 101
    
#     for certificate in certificates:
        
        # certificate_domains = ssl_get_managed_domains(certificate)
#         domain_count = len(certificate_domains)
        
#         if domain_count < smallest_domain_count and domain_count < 100:
#             # smallest_certificate = certificate
#             smallest_certificate_domains = certificate_domains
#             smallest_domain_count = domain_count

#         # temp = {"name":certificate_name,"managed":{"domains":certificate_domains}}
#         # certi_list.append(temp)
#         # if len(certi["managed"]["domains"]) >= len(temp["managed"]["domains"]):
#             # certi = temp        
#         # sorted_data = sorted(data, key=lambda x: len(x.get('name', '')))


#     new_certificate_domains = smallest_certificate_domains[:]
#     new_certificate_domains.append(new_domain)

#     # de-deplicating domains
#     new_certificate_domains = list(set(new_certificate_domains))
    
#     # new_certificate = certificate_name
#     new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
    
    
#     # ssl_create_managed(certificate_name = new_certificate, domains=new_certificate_domains)
    
#     # certificates.remove(smallest_certificate)
#     certificates.append(new_certificate)

#     # x = https_proxy_attach_ssl_certificate(certificates)

#     # print(certi_list)
#     # certi["managed"]["domains"].append(new_domain)
#     # list_domain=certi["managed"]["domains"]
    
#     # return list_domain,certis
#     return new_certificate_domains, certificates

#===============================================================================


def domain_list(new_domain: str,certificate_name: str):
    # print(lb)
    all_certificates = https_proxy_get(load_balancer=lb)
    
    dic1 = {}
    latest_certificate = None
    latest_timestamp = None

    for i in all_certificates:
          print("start")
          max_timestamp,domains, = ssl_get_managed_domains(i)
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

    print("latest",latest_certificate)
    if latest_certificate and cnt_domain < 99 :
        domains_to_merge = []
        for certificate, data in dic1.items():
            if certificate != latest_certificate and len(data[1]) != 99:
                domains_to_merge.extend(data[1])

        dic1[latest_certificate][1].extend(domains_to_merge)
        dic1[latest_certificate][1] = list(set(dic1[latest_certificate][1]))

        new_certificate_domains= list(dic1[latest_certificate][1])
        new_certificate_domains.append(new_domain)
        all_certificates=[]
        all_certificates = list(dic1.keys())
        new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
        all_certificates.append(new_certificate)
        

        return new_certificate_domains, all_certificates
    
    else:
        all_certificates = []
        new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
        all_certificates.append(latest_certificate)
        all_certificates.append(new_certificate)

        new_certificate_domains = []
        new_certificate_domains.append(new_domain)
        print('after 99 ',new_certificate_domains, all_certificates)    

        return new_certificate_domains, all_certificates

