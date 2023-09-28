from fastapi import Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
import os
import re
from google.cloud import run_v2
from google.iam.v1 import iam_policy_pb2
from lib.RUN import create_service_tagging, create_service_preview_tagging, sample_set_iam_policy
from lib.SSL import ssl_create_managed
from lib.LB import *
from lib.DomainList import domain_list
# project_id="server-side-tagging-392006"


router = APIRouter()


@router.post('/create')
async def sst_create(request: Request):
    payload_bytes = await request.body()
    print(payload_bytes)
    payload_str = payload_bytes.decode("utf-8")
    queryParams = json.loads(payload_str)
    print(queryParams)

    store_id = queryParams.get('store_id')
    region = queryParams.get('region')
    domain = queryParams.get('domain')
    container_config = queryParams.get('container_config')

    print("name", store_id)
    print("region", region)
    print("container_config", container_config)

    preview_server_url, preview_name = await create_service_preview_tagging(store_id, region, container_config)
    sample_set_iam_policy(preview_name)
    result1, tagging_name, details = await create_service_tagging(store_id, region, container_config, preview_server_url)
    sample_set_iam_policy(tagging_name)

    certificate_name = f'sst-{store_id}-certificate'
    print(certificate_name)
    list_domain, certis = domain_list(domain, certificate_name)
    ssl_create_managed(certificate_name=certificate_name, domains=list_domain)
    # Function to check state of newly created certificate to be added
    https_proxy_attach_ssl_certificate(certificate_urls=certis)
    # Works till here Rev: test-backend-sst-lb-00018-lrx #

    # Latest revision additions Rev: test-backend-sst-lb-00019
    cloud_run_name = tagging_name
    backend_service_name = f"{cloud_run_name}_be"
    neg_name = f"{cloud_run_name}_neg"

    neg_create_regional_cloud_run(region=region, neg_name=neg_name, cloud_run_service_name= cloud_run_name)
    backend_create_global(backend_service_name=backend_service_name, neg_name = neg_name, neg_region=region)
    hostrule_add(domain=[domain], backend_service_name=backend_service_name, paths=["/test", "/dev", "/pre-prod"])

    return {"Payload Details": details}
