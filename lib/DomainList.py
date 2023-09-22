import configparser
from lib.LB import *
from lib.SSL import *


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]


def domain_list(new_domain: str,certificate_name: str):
    certis = https_proxy_get(load_balancer=lb)
    certi_list = []

    for item in certis:
        certificate_domains = ssl_get_managed_domains(item)
        temp = {"name":certificate_name,"managed":{"domains":certificate_domains}}
        certi_list.append(temp)
        if len(certi["managed"]["domains"]) >= len(temp["managed"]["domains"]):
            certi = temp        
        # sorted_data = sorted(data, key=lambda x: len(x.get('name', '')))

    print(certi_list)
    certi["managed"]["domains"].append(new_domain)
    list_domain=certi["managed"]["domains"]
    return list_domain,certis

    