FROM prefecthq/prefect:2.7.7-python3.9 as base

FROM base as agent

COPY requirements.txt .

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install  psycopg2-binary s3fs && \
    pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

RUN mkdir -p /opt/prefect/data
WORKDIR /opt/prefect
CMD ["python", "flows/01_start/ingest_data.py"]