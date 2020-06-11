# Gunicorn image
FROM python:3.8.3-slim-buster as core

ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    # iproute2 is needed for Django debug toolbar 
    iproute2 \
    gdal-bin \
    libproj-dev \
    libsqlite3-mod-spatialite \
    locales \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
