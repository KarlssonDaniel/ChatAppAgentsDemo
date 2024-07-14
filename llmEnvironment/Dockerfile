FROM python:3.11-slim

WORKDIR /code


COPY ./requirements.txt ./

RUN apt update && \
apt install -y git && \
apt clean 

RUN pip install --no-cache-dir -r requirements.txt


