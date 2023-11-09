#Base Image
FROM python:3.10.7-slim-buster

#change working directory
WORKDIR /app

#copy requirements.txt to install all the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#copy source code
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --timeout 220  --worker-class uvicorn.workers.UvicornWorker --threads 8 delete:app