FROM python:latest

COPY ./requirements.txt requirements.txt

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple --trusted-host pypi.douban.com