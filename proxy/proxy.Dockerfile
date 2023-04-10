FROM python:latest

COPY . /proxy/
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /proxy/