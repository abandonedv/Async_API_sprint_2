FROM python:3.11-slim

WORKDIR /home/server

COPY requirements.txt .

RUN pip install --no-cache-dir -U pip setuptools wheel \
 && pip install --no-cache-dir -Ur requirements.txt

COPY . ./app

CMD gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
