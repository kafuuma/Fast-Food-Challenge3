FROM python:3.7-alpine
MAINTAINER Henry "arkafuuma@gmail.com"
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install python3.7-dev 
RUN pip install -r requirements.txt
CMD ["python","run.py"]
