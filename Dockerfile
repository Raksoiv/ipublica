FROM python:3-alpine

WORKDIR /src
COPY requirements.txt requirements.txt
RUN apk update && apk add --no-cache alpine-sdk
RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache -r requirements.txt
COPY . .
