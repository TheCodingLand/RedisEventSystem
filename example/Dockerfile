FROM python:latest

RUN apt-get update && apt-get upgrade

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

ADD . /usr/src/app
CMD python3 main.py