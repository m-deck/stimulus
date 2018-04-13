FROM python:3
MAINTAINER michaelanthonydeck@gmail.com

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

RUN apt-get clean && apt-get update
RUN apt-get -y install build-essential libsasl2-dev
RUN apt-get -y install freetds-dev
RUN mkdir /code

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/