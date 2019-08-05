FROM python:3-alpine

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
