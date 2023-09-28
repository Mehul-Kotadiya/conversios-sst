from google.cloud import compute_v1
from lib.SSL import *
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]

client = compute_v1.TargetHttpsProxiesClient()
compute_client = compute_v1.InstancesClient()


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

def https_proxy_attach_ssl_certificate(certificate_urls):

    # compute_service = build('compute', 'v1', credentials=credentials)
    # client = compute_v1.TargetHttpsProxiesClient()

    # load_balancer_name = 'test-lb-target-proxy'
    # certificate_urls=[]
    # for item in certis:
    #     certificate_urls.append(f'https://www.googleapis.com/compute/v1/projects/{project_id}/global/sslCertificates/{item}')

    # new_certificate_url=f'https://www.googleapis.com/compute/v1/projects/{project_id}/global/sslCertificates/{new_certificate_name}'

    # certificate_urls.append(new_certificate_url)
    

    request_body = {
        'ssl_certificates': certificate_urls
    }

    # Initialize request argument(s)
    request = compute_v1.SetSslCertificatesTargetHttpsProxyRequest(
        project= project,
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

def backend_create_global(backend_service_name: str, neg_name: str, neg_region: str):

    # Create a client
    client = compute_v1.BackendServicesClient()

    base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{neg_region}".format(project, neg_region)
    neg_url = f"{base_url}/networkEndpointGroups/{neg_name}".format(neg_name)

    # neg_url = f"projects/{project}/global/networkEndpointGroups/{neg_name}".format(project, region, neg_name)

    # Initialize request argument(s)
    request = compute_v1.InsertBackendServiceRequest(
        backend_service_resource=compute_v1.BackendService(
            name=backend_service_name,
            protocol="HTTPS",
            load_balancing_scheme="EXTERNAL_MANAGED",
            backends=[compute_v1.Backend(group=neg_url)]
        ),
        project=project
    )

    # Make the request
    response = client.insert(request=request)
    response = response.result()
    return response

def backend_create_regional(region: str, backend_service_name: str, neg_name: str):

    base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}".format(project, region)
    neg_url = f"{base_url}/networkEndpointGroups/{neg_name}".format(neg_name)

    client = compute_v1.RegionBackendServicesClient()

    # Initialize request argument(s)
    request = compute_v1.InsertRegionBackendServiceRequest(
        project=project,
        region=region,
        backend_service_resource = compute_v1.BackendService(
            name=backend_service_name,
            protocol="HTTPS",
            load_balancing_scheme="EXTERNAL_MANAGED",
            backends=[compute_v1.Backend(group=neg_url)]
        ),
    )

    # Make the request
    response = client.insert(request=request)
    response = response.result()
    # Handle the response
    return response

def neg_create_regional_cloud_run(region: str, neg_name: str, cloud_run_service_name: str):
    request = compute_v1.InsertRegionNetworkEndpointGroupRequest(
        project=project,
        region=region,

        network_endpoint_group_resource=compute_v1.NetworkEndpointGroup(
            name=neg_name,
            network_endpoint_type="SERVERLESS",

            cloud_run=compute_v1.NetworkEndpointGroupCloudRun(
                service=cloud_run_service_name
            )
        )
    )

    client = compute_v1.RegionNetworkEndpointGroupsClient()
    response = client.insert(request)
    response = response.result()
    return response

def urlmap_get(lb: str):
    # Create a client
    client = compute_v1.UrlMapsClient()

    # Initialize request argument(s)
    request = compute_v1.GetUrlMapRequest(
        project=project,

        # .replace("-target-proxy","")
        url_map=lb
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    return response

def hostrule_add(domain: list, backend_service_name: str, paths: list = ["/test"]):
    
    
    new_lb = lb.replace("-target-proxy","")
    urlMapObj = urlmap_get(lb = new_lb)
    # backend_service_name = backend_name
    base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/global".format(project)
    backend_url = f"{base_url}/backendServices/{backend_service_name}".format(project, backend_service_name)


    # add some random name, can we keep it static?
    path_matcher_name = "path-1"

    pathMatcherObj = compute_v1.PathMatcher(
        default_service=backend_url,
        name=path_matcher_name,
        path_rules=[compute_v1.PathRule(service = backend_url, paths = paths)]
    )
    hostRule = compute_v1.HostRule(hosts=domain, path_matcher=path_matcher_name)


    urlMapObj.path_matchers.append(pathMatcherObj)
    urlMapObj.host_rules.append(hostRule)

    request = compute_v1.UpdateUrlMapRequest(
        project=project,
        
        # wtf is this, probably Load balancer?
        url_map=new_lb,
        url_map_resource=urlMapObj
    )

    # Make the request
    client = compute_v1.UrlMapsClient()
    response = client.update(request=request)
    response = response.result()

    # Handle the response
    return response

# load_balancer = https_proxy_get()
# print(load_balancer)
# for certi in load_balancer.ssl_certificates:
#     domains = ssl_get_managed_domains(certi)
#     print(domains)

# x = https_proxy_attach_ssl_certificate()
# print(x)
