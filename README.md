# property-maintenance

## Apache Superset Dashboard
<img width="941" alt="image" src="https://github.com/user-attachments/assets/d40092c7-b67e-4376-97c5-8466e7bc2566" />

## Reproduce
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
