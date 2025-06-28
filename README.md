## Overview
Designed and implemented a fully automated data pipeline and analytics solution for property maintenance data using modern data stack tools including:

- Apache Airflow - for orchestrating a Python-based workflow for loading CSV data from Google Cloud Storage (GCS) into Google BigQuery.

- DBT - to build modular data transformations, generic and custom data tests to validate data integrity, and documentation for model transparency. Also scheduled daily model runs and tests using a DBT cloud job to ensure consistent data freshness and data quality in production.

- Apache Superset - to integrate with BigQuery for delivering key business insights such as: top regions by property count, repair cost trends and properties over 5 years old with lower average repair costs.

- Docker - to containerize all components for consistent local development and production deployment.

## Solution Architecture
![final](https://github.com/user-attachments/assets/24d76555-431e-48a9-8131-88c47d234f9f)

## Data Lineage
<img width="832" alt="image" src="https://github.com/user-attachments/assets/85ed881a-7cc1-4909-8bb5-91ecea337a5a" />

## Apache Superset Dashboard
<img width="941" alt="image" src="https://github.com/user-attachments/assets/d40092c7-b67e-4376-97c5-8466e7bc2566" />

## Reproduction Steps
To reproduce, clone this repository and run these commands in the root directory of the repo's folder (/property-maintenance)

### 1. Build Docker image
This builds the custom Airflow image with your Dockerfile

`docker-compose build`

### 2. Initialize the Airflow metadata database

`docker-compose up airflow-init`

This will:

- Run DB migrations
- Create the admin user (airflow:airflow unless overridden)
- Set permissions on volumes

### 3. Start all services

`docker-compose up -d`

This will start Airflow webserver, scheduler, workers, Redis, Postgres, and Superset

### 4. Optional but recommended
You might want to check logs during first runs:

`docker-compose logs -f`

And if Superset didn't initialize properly, you can force it manually:

`docker-compose run --rm superset-init`

### 5. Extra Tips
Want to reset Airflow state? Delete the volumes:

`docker-compose down -v`

Rebuild after editing Dockerfile:

`docker-compose build --no-cache`
