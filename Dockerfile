FROM python:3.10-buster

WORKDIR /src

COPY requirements.txt /src
RUN pip install -r requirements.txt

COPY . /src

