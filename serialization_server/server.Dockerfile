FROM python:latest

COPY . /serialization_server/

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /serialization_server/