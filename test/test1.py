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

    all_certificates = https_proxy_get(load_balancer=lb)
    dic1 = {}

    latest_certificate = None
    latest_timestamp = None

    for i in all_certificates:
          print("start")
          max_timestamp,domains, = ssl_get_latest_domains_(i)
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


# Merge domains of all previous all_certificates into the latest one
    print("latest",latest_certificate)
    if latest_certificate and cnt_domain < 99 :
        
        domains_to_merge = []
        for certificate, data in dic1.items() :
            if certificate != latest_certificate  and len(data[1]) != 99:
             
                domains_to_merge.extend(data[1])
                
       
        dic1[latest_certificate][1].extend(domains_to_merge)
        dic1[latest_certificate][1] = list(set(dic1[latest_certificate][1]))

        new_certificate_domains= list(dic1[latest_certificate][1])
        new_certificate_domains.append(new_domain)
        all_certificates=[]
        all_certificates = list(dic1.keys())
        new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
        all_certificates.append(new_certificate)
        
        print(new_certificate_domains)

        return new_certificate_domains, all_certificates
    
    else:
        all_certificates = []
        new_certificate = f'https://www.googleapis.com/compute/v1/projects/{project}/global/sslCertificates/{certificate_name}'.format(project,certificate_name)
        all_certificates.append(latest_certificate)
        all_certificates.append(new_certificate)
        print('after 99 ',new_domain, all_certificates)    
        return new_domain, all_certificates


if __name__ == "__main__":
    timestamp1= round(time.time()*1000)
    certificate_name = f'sst-certificate-{timestamp1}'
    new_certificate_domains, all_certificates = domain_list("deep.com",certificate_name)

# domains=['N1Sz9Q2.com','5MEmex5.com','1tBW83Y.com','h99rTXcE76.com','A9c4o0geQq.com','D9A9276.com','C5l3149.com','w65H9i9.com','ZR13aDcOwE.com','wIyzjehmNj.com','A9yq889.com','732q8IE.com','Xp694EC.com','835tduC.com','Q7c5I1iesl.com','P4Cv8kF.com','YV8a9xO.com','H0rD5R8.com','kJnkpAg5kV.com','Q8lT4x9.com','Qp7q9eS.com','5kA6N9yYox.com','l72x67Z.com','6aSs8GrD28.com','4H80WWn8iM.com','XCGtlIaxCb.com','74aUZ1dhT2.com','z1ZVS7C.com','HIA7J95.com','jve48WZ.com','dK5yCtjPIO.com','UV5XYoO.com','7A3sfPZ.com','cyOZYLg8rl.com','nPBUYArWxC.com','Y72e9w6.com','IUh6jjL.com','88uVALt8Pc.com','0Ol32nuv1T.com','65Ewg30.com','A7WzkhC.com','x72J5adod8.com','x91j74faQf.com','L5CQG36.com','27wh3oP.com','MiNeDDpcul.com','iZ25om3.com','D1M1bi6.com','BggivTl338.com','s83r9BT.com','qaxyiJX.com','9ho7o9G.com','EDkvg1D.com','PNQyu03.com','KBE2s9U.com','0RoqDb2.com','Y5N834E.com','q7Tieppxsj.com','9EweovD.com','n9ixT9N.com','zuJT5wumTL.com','NCT72OO.com','7P5aDVX.com','BPuXJDE.com','YcXJ19ogC8.com','502fdG9.com','o8rwmGR.com','s9tN23txOQ.com','v5YLfJD.com','753mJ9nPFD.com','E0BSJm5.com','E2Bgi6Z.com','N3X8g2F.com','G08r21V.com','5Z6pKgh0fE.com','bq1n8p1.com','NuFVMpC.com','BT0cYQ1.com','Wt93ATN.com','9DGssXjz2m.com','yYuh75O.com','sTvAhXzjM4.com','qJ33F9O.com','xkCekI4.com','dC2gcU3.com','C5iO10q37S.com','dgi9jna070.com','7T3zW4D.com','B1I9iJ1.com','961684H.com','0hw892F.com','6j0CfQM.com','u22phl8.com','l67IJy0.com','1N45L35.com','Rm3wEe1.com','VkkJ698.com','mDT8BB6.com','4coQm7f8lN.com',]
# ssl_create_managed(domains)
# print(new_certificate_domains, all_certificates )

# # Read input data from a JSON file
# with open('/home/yash/Desktop/sony_iam.json', 'r') as input_file:
#     items = json.load(input_file)

# # Serialize each item as JSON and join with newline characters
# with open('/home/yash/Desktop/sony_iam_output.json', 'w') as output_file:
#     for i in items:
#         # Serialize the current item as JSON and write it as a separate line
#         json_string = json.dumps(i)
#         output_file.write(json_string+"\n")

# ['https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-10004-certificate-1700133547187', 
#  'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-13027-certificate-1700560873502', 
#  'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-10004-certificate-1900133547187']
