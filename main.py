import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from google.cloud import run_v2
from google.cloud import datastore
import datetime


# client = datastore.Client()

 
from routers import final

#create FastAPI app
app = FastAPI(
    title="Backend Application to deploy and maintain multiple SSGTM",
    description= "Backend Application to deploy and maintain multiple SSGTM created via conversios frontend",
    version="1.0.0"
)


#add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/")
async def root():
    """" Application Home """
    logging.debug('Home Get method called.....')
    return {"message": "Hello World"}


app.include_router(final.router,prefix='/sst',tags=['SSTmain'])



# @app.post("/my-update")
# async def update(request:Request):
#     # project_id = 'server-side-tagging-392006'
#     # location = 'asia-east1'  # Cloud Run region
#     # service_name = 'sst-13485-00001-l2w'
#     payload_bytes = await request.body()
#     print(payload_bytes)
#     payload_str = payload_bytes.decode("utf-8")
#     queryParams = json.loads(payload_str)
#     print(queryParams)



#     store_id = queryParams.get('store_id')
    ## region = queryParams.get('region')
#     domain = queryParams.get('domain')
#     container_config = queryParams.get('container_config')

#     # print("name", store_id)
#     # print("region", region)
#     # print("container_config", container_config)

#     kind = 'server-side-tagging'
#     parent_key=None
#     custom_key = client.key(kind,str(store_id),parent=parent_key)
#     entity = datastore.Entity(key=custom_key)

#     entity["name"]=store_id
#     entity['region']=region
#     entity['domain']=domain
#     entity['container_config']=container_config
#     client.put(entity)

#     # query = client.query(kind="1234")
#     # val=list(query.fetch())
#     # if val:
#     #     v = val[0]
#     #     name = v['name']
#     #     print(name)

#     # else:
#     #     print("not found")


#     run_client = run_v2.ServicesClient()
#     request=run_v2.UpdateServiceRequest(
#         service = {
            
#             "name" : "projects/server-side-tagging-392006/locations/asia-south1/services/sst-55555",
#             "ingress": "INGRESS_TRAFFIC_ALL",
#             "template": {
#                 "scaling":{
#                     "min_instance_count":1,
#                     "max_instance_count":2    
#                 },
#                 "containers": [{
#                     "image": "gcr.io/cloud-tagging-10302018/gtm-cloud-image:stable",
#                     "resources": {
#                         "cpu_idle": False
#                     },
#                     "env": [{
#                         "name": "CONTAINER_CONFIG",
#                         "value": "aWQ9R1RNLVdKM0hDRlczJmVudj0xJmF1dGg9dHpjMGMzc0VUVnA1M1RsNlotNlFjZw=="
#                     }]
                    
#                 }],
#                 "timeout":{
#                     "seconds": 60
#                 }
#             }
#         }  
#     )
#     # operation = run_client.update_service(metadata= [("name", "sst-55555")],request=request)

#     # print(operation.result)


#     return "hello"





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

