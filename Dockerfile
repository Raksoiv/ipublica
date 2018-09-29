FROM python:3-alpine

WORKDIR /ipublica
COPY requirements.txt requirements.txt
RUN apk update && apk add --no-cache alpine-sdk libxml2-dev libxslt-dev libffi-dev libressl-dev
RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache -r requirements.txt
COPY . .
