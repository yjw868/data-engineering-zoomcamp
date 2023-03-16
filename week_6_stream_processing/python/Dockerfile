FROM python:3.8.5-slim AS base

COPY requirements.txt .

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y curl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

WORKDIR /opt/cli/