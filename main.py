import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


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

