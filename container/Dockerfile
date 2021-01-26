# FROM jupyter/datascience-notebook:latest 
FROM python:3.7.9

RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib curl nginx

COPY docker_requirements.txt requirements.txt
RUN pip install -r requirements.txt

# AWS sagemaker bindings
# /opt/ml and all subdirectories are utilized by SageMaker, we use the /code subdirectory to store our user code.
ENV PATH="/opt/ml/code:${PATH}"
COPY /example /opt/ml/code
WORKDIR /opt/ml/code

