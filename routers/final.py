from fastapi import Request,APIRouter
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
import os 
import re
from google.cloud import run_v2

project_id="server-side-tagging-392006"

router=APIRouter()

@router.post('/create')
async def sst_create(request: Request):
    payload_bytes= await request.body()  
    print(payload_bytes)  
    payload_str = payload_bytes.decode("utf-8") 
    queryParams = json.loads(payload_str)
    print(queryParams)     
    store_id = queryParams.get('store_id')
    region = queryParams.get('region')
    container_config = queryParams.get('container_config')
    print("name",store_id)
    print("region",region)
    print("container_config",container_config)
    preview_server_url=await create_service_preview_tagging(store_id,region,container_config)
    result1=await create_service_tagging(store_id,region,container_config,preview_server_url)
    return {"server_url": result1}

# location="asia-south1"
# project_id=os.getenv("PROJECT_ID")
# location=os.getenv("LOCATION")
# name=os.getenv("NAME")
# name="dem66"

async def create_service_preview_tagging(store_id: str,region:str,container_config:str):
    run_client = run_v2.ServicesClient()
    suffix="-preview"
    request = run_v2.CreateServiceRequest(
        parent=f"projects/{project_id}/locations/{region}",
        service_id="sst-"+store_id+suffix,
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
                        "value": container_config
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

    operation = run_client.create_service(metadata= [("name", "sst-"+store_id+suffix)],request=request)
    print("Setting up preview server")
    response = operation.result()
    preview_url_value=response.uri
    # print(preview_url_value)
    print("Preview_Server Response:",response)
    
    # cont=str(response.template.containers)
    # match = re.search(r'name: "CONTAINER_CONFIG"\s+value: "(.*?)"', cont)
    # if match:
    #     container_config_value = match.group(1)
    #     # print(container_config_value)
    # else:
    #     print("CONTAINER_CONFIG not found in the input string.")
    
    return preview_url_value


async def create_service_tagging(store_id,region,container_config,preview_server_url):
    run_client = run_v2.ServicesClient()

    request = run_v2.CreateServiceRequest(
        parent=f"projects/{project_id}/locations/{region}",
        service_id="sst-"+store_id,
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
                        "value": container_config
                        },
                        {"name": "PREVIEW_SERVER_URL",
                        "value": preview_server_url,
                    }]
                    
                }],
                "timeout":{
                    "seconds": 60
                }
            }
        }    
    )

    operation = run_client.create_service(metadata= [("name", "sst-"+store_id)],request=request)
    print("Setting up server side tagging...")
    response = operation.result()
    server_url_value=response.uri
    nt=(str(response.name)).split("services/")[1]
    print("Name of server:",nt)
    print("Server_url",server_url_value)
    print("Tagging server:",response)
    return server_url_value,nt


if __name__ == "__main__":
    uvicorn.run("test:app", host="127.0.0.1", port=8000,reload=True)