FROM apache/airflow:2.10.5

USER root
# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        procps \
        curl \
        build-essential \
        python3-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

# Install python dependencies individually
RUN pip install --no-cache-dir apache-airflow-providers-google>=2.9.0 psycopg2-binary