from google.cloud import compute_v1

import configparser


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]
lb = config["gcp"]["load_balancer"]


# x = compute_v1.UrlMap(name="new_temp", default_service = "backend-service-using-python-new-new")
# print(x)

def urlmap_insert():
    # Create a client
    client = compute_v1.UrlMapsClient()

    # Initialize request argument(s)
    request = compute_v1.InsertUrlMapRequest(
        project=project,
        url_map_resource=compute_v1.UrlMap(
            name="new-temp", default_service="https://www.googleapis.com/compute/v1/projects/tatvic-gcp-dev-team/global/backendServices/backend-service-using-python-new-new")
    )

    # Make the request
    response = client.insert(request=request)

    # Handle the response
    return response


def urlmap_set_https_proxy():
    # Create a client
    client = compute_v1.TargetHttpsProxiesClient()

    url_map_reference = f'projects/{project}/global/urlMaps/new-temp'

    # Initialize request argument(s)
    request = compute_v1.SetUrlMapTargetHttpsProxyRequest(
        project=project,
        target_https_proxy="test-lb-target-proxy",
        url_map_reference_resource=compute_v1.UrlMapReference(
            url_map=url_map_reference)
    )

    # Make the request
    response = client.set_url_map(request=request)

    # Handle the response
    return response


def backend_get():
    # Create a client
    client = compute_v1.BackendServicesClient()

    # Initialize request argument(s)
    request = compute_v1.GetBackendServiceRequest(
        backend_service="backend-service-using-python-new-new",
        project=project,
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    return response


def urlmap_get():
    # Create a client
    client = compute_v1.UrlMapsClient()

    # Initialize request argument(s)
    request = compute_v1.GetUrlMapRequest(
        project=project,
        url_map=lb
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    return response


def hostrule_add(domain: list, backend_name: str, paths: list = ["/*"]):
    urlMapObj = urlmap_get()

    backend_service_name = backend_name
    backend_name = f"https://www.googleapis.com/compute/v1/projects/{project}/global/backendServices/{backend_service_name}".format(project, backend_service_name)


    # add some random name, can we keep it static?
    path_matcher_name = "pm1"

    pathMatcherObj = compute_v1.PathMatcher(
        default_service=backend_name,
        name=path_matcher_name,
        path_rules=[compute_v1.PathRule(service = backend_name, paths = paths)]
    )
    hostRule = compute_v1.HostRule(hosts=domain, path_matcher=path_matcher_name)


    urlMapObj.path_matchers.append(pathMatcherObj)
    urlMapObj.host_rules.append(hostRule)

    request = compute_v1.UpdateUrlMapRequest(
        project=project,
        
        # wtf is this, probably Load balancer?
        url_map="test-lb",
        url_map_resource=urlMapObj
    )

    # Make the request
    client = compute_v1.UrlMapsClient()
    response = client.update(request=request)

    # Handle the response
    print(response)

cloud_run_service_name = 'hello'
url_map_name = 'trail-url-map'
target_https_proxy_name = ''

region = "asia-south1"

backend_service_name = 'temp-be'
neg_name = 'temp-neg'
regional_base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}".format(project, region)
global_base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/global".format(project, region)

neg_url = f"{regional_base_url}/networkEndpointGroups/{neg_name}".format(project, region, neg_name)
backend_url = f"{global_base_url}/backendServices/{backend_service_name}".format(project, backend_service_name)


def backend_create_global(backend_service_name: str, neg_name: str):

    # Create a client
    client = compute_v1.BackendServicesClient()

    base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/global".format(project, region)
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

def neg_create_regional_cloud_run(region: str, neg_name: str):
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

def urlmap_get():
    # Create a client
    client = compute_v1.UrlMapsClient()

    # Initialize request argument(s)
    request = compute_v1.GetUrlMapRequest(
        project=project,
        url_map=lb
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    return response

def hostrule_add(domain: list, backend_service_name: str, paths: list = ["/test"]):
    urlMapObj = urlmap_get()

    # backend_service_name = backend_name
    base_url = f"https://www.googleapis.com/compute/v1/projects/{project}/global".format(project, region)
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
        url_map=lb,
        url_map_resource=urlMapObj
    )

    # Make the request
    client = compute_v1.UrlMapsClient()
    response = client.update(request=request)
    response = response.result()

    # Handle the response
    return response
