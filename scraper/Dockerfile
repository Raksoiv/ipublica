FROM python:3-slim

WORKDIR /src
COPY setup.py requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install -e .

COPY ./scripts ./scripts
COPY ./scraper ./scraper
