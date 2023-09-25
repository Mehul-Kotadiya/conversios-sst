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
