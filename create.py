from google.cloud import run_v2
import os
import re


# project_id="server-side-tagging-392006"
# location="asia-south1"
# GOOGLE_APPLICATION_CREDENTIALS="/home/jeet/internal/Conversios/development/creds.json"
project_id=os.getenv("PROJECT_ID")
location=os.getenv("LOCATION")
name=os.getenv("NAME")
name="dem66"
# GOOGLE_APPLICATION_CREDENTIALS=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/jeet/internal/Conversios/development/creds.json"

def create_service_preview_tagging():
    run_client = run_v2.ServicesClient()
    suffix="-preview"
    request = run_v2.CreateServiceRequest(
        parent=f"projects/{project_id}/locations/{location}",
        service_id="sst-"+name+suffix,
        service = {
            "ingress": "INGRESS_TRAFFIC_ALL",
            # "traffic": {
            #     "type_":"TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
            #     "percent": 100
            # },
            "template": {
                "scaling":{
                    "min_instance_count":0,
                    "max_instance_count":1    
                },
                "containers": [{
                    "image": "gcr.io/cloud-tagging-10302018/gtm-cloud-image:stable",
                    "resources": {
                        "cpu_idle": False
                    },
                    "env": [{
                        "name": "CONTAINER_CONFIG",
                        "value": "aWQ9R1RNLU5EWlRTRE0mZW52PTEmYXV0aD1ma0hfRHNyOWk1YmZQT1dvSGxyY0Zn"
                        },
                        {"name": "RUN_AS_PREVIEW_SERVER",
                        "value": 'true',
                    }]
                    
                }],
                "timeout":{
                    "seconds": 60
                }
            }
        }    
    )

    operation = run_client.create_service(metadata= [("name", "sst-"+name)],request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    preview_url_value=response.uri
    # print(preview_url_value)
    
    cont=str(response.template.containers)
    match = re.search(r'name: "CONTAINER_CONFIG"\s+value: "(.*?)"', cont)
    if match:
        container_config_value = match.group(1)
        # print(container_config_value)
    else:
        print("CONTAINER_CONFIG not found in the input string.")
    
    return preview_url_value,container_config_value


def create_service_tagging(par1,par2):
    run_client = run_v2.ServicesClient()

    request = run_v2.CreateServiceRequest(
        parent=f"projects/{project_id}/locations/{location}",
        service_id="sst-"+name,
        service = {
            "ingress": "INGRESS_TRAFFIC_ALL",
            # "traffic": {
            #     "type_":"TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
            #     "percent": 100
            # },
            "template": {
                "scaling":{
                    "min_instance_count":1,
                    "max_instance_count":2    
                },
                "containers": [{
                    "image": "gcr.io/cloud-tagging-10302018/gtm-cloud-image:stable",
                    "resources": {
                        "cpu_idle": False
                    },
                    "env": [{
                        "name": "CONTAINER_CONFIG",
                        "value": par2
                        },
                        {"name": "PREVIEW_SERVER_URL",
                        "value": par1,
                    }]
                    
                }],
                "timeout":{
                    "seconds": 60
                }
            }
        }    
    )

    operation = run_client.create_service(metadata= [("name", "sst-"+name)],request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    print("tagging server",response)
    

result1,result2=create_service_preview_tagging()
print(result1,result2)

create_service_tagging(result1,result2)
