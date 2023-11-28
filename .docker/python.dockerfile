FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get install -y libpq-dev python-dev

RUN pip install psycopg2-binary

WORKDIR /app