FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /task/src
WORKDIR /task/src

ADD requirements.txt /task/src/

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

ADD ../ /task/src  
WORKDIR /task/src/task