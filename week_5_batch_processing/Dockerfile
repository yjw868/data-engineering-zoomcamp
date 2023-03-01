FROM docker.io/bitnami/spark:3.3.2 as base

ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

USER root
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir 
RUN groupadd -r spark && useradd -m -r -g spark spark
RUN chown -R spark:spark /opt/bitnami/spark
RUN mkdir /.local/share # for jupyter
RUN chown -R spark:spark /.local/share
# RUN chown -R spark:spark /opt/bitnami/
# USER spark
WORKDIR /opt/spark-apps


