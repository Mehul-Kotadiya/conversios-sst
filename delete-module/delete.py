from google.cloud import compute_v1
import os
import configparser
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
async def batch_function ():
    config = configparser.ConfigParser()
    config.read('config.ini')
    project = config["gcp"]["project_id"]
    lb = config["gcp"]["load_balancer"]
    proxy_name="-target-proxy"


    client = compute_v1.SslCertificatesClient()
    ssl_certificates = client.list(project=project)
    my_domain = 'newdomain2.com'
    json_formatted_data = []
    certi_status=[]

    for cert in ssl_certificates:
        name = cert.name
        status = cert.managed.status
        domains = cert.managed.domains

        certificate_data = {
            'name': name,
            'domain': domains,
            'status': status,
        }

        json_formatted_data.append(certificate_data)
        print(json_formatted_data)
    return {"message": "complete the scan   "}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    batch_function()

# for i in json_formatted_data:
#     if 'example.com' in i['domain']:
#         certi_status.append(i['status'])

# for cert in certi_status:
#     if cert=='Provisioning':
#         print('Active')
#     else:
#         print(cert)