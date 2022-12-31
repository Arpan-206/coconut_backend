# base image  
FROM python:3.9
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip 
COPY . $DockerHOME

RUN pip install .

EXPOSE 80

CMD ["gunicorn", "coconut_backend.main:app", "--worker-class",  "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:$PORT"]
