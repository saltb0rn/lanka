FROM python:latest

WORKDIR /srv/music.api

COPY ./requirements.txt requirements.txt

#RUN apk update
#RUN apk add gcc
#RUN apk add python3-dev
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple --trusted-host pypi.douban.com