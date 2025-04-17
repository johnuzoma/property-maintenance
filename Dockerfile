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
RUN pip install --no-cache-dir boto3>=1.28.0 && \
    pip install --no-cache-dir apache-airflow-providers-postgres>=5.0.0 && \
    pip install --no-cache-dir pandas>=2.0.0 && \
    pip install --no-cache-dir pyarrow>=14.0.0 && \
    pip install --no-cache-dir sqlalchemy>=2.0.0 && \
    pip install --no-cache-dir psycopg2-binary>=2.9.0