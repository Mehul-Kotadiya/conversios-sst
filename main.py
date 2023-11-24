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



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8080, reload=True)

