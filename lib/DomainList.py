import configparser
from lib.LB import *
from lib.SSL import *


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]


def domain_list(new_domain: str,certificate_name: str):
    print(lb)
    certificates = https_proxy_get(load_balancer=lb)
    # certi_list = []
    # smallest_certificate = None
    smallest_domain_count = 101
    
    for certificate in certificates:
        
        certificate_domains = ssl_get_managed_domains(certificate)
        domain_count = len(certificate_domains)

        if domain_count < smallest_domain_count and domain_count < 100:
            # smallest_certificate = certificate
            smallest_certificate_domains = certificate_domains
            smallest_domain_count = domain_count

        # temp = {"name":certificate_name,"managed":{"domains":certificate_domains}}
        # certi_list.append(temp)
        # if len(certi["managed"]["domains"]) >= len(temp["managed"]["domains"]):
            # certi = temp        
        # sorted_data = sorted(data, key=lambda x: len(x.get('name', '')))


    new_certificate_domains = smallest_certificate_domains[:]
    new_certificate_domains.append(new_domain)

    # de-deplicating domains
    new_certificate_domains = list(set(new_certificate_domains))
    
    # new_certificate = certificate_name
    new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
    
    
    # ssl_create_managed(certificate_name = new_certificate, domains=new_certificate_domains)
    
    # certificates.remove(smallest_certificate)
    certificates.append(new_certificate)

    # x = https_proxy_attach_ssl_certificate(certificates)

    # print(certi_list)
    # certi["managed"]["domains"].append(new_domain)
    # list_domain=certi["managed"]["domains"]
    
    # return list_domain,certis
    return new_certificate_domains, certificates
    

    