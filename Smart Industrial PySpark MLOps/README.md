# Smart Industrial Data Engineering & Predictive Maintenance Platform

A GitHub-ready portfolio project using PySpark for industrial sensor ETL and Spark ML predictive maintenance, with PostgreSQL, FastAPI, MLflow, Prometheus, Grafana, Docker and Pytest.

## Architecture

```text
Industrial Sensor CSV
        |
        v
+-------------------+
|      PySpark      |
| Clean / Transform |
| Feature Engineer  |
+---------+---------+
          |
          +--------------------+
          |                    |
          v                    v
    Processed Parquet     Spark MLlib
                               |
                               v
                         Failure Model
                               |
                               v
                         Predictions
                               |
                               v
                         PostgreSQL
                               |
                    +----------+----------+
                    |                     |
                    v                     v
                 FastAPI              Grafana
                    |                     ^
                    v                     |
               REST API <---------- Prometheus
                    |
                    v
                 MLflow
```

## Dataset

Expected file: `data/raw/machine_sensor_data.csv`

Columns:

`machine_id, timestamp, temperature, vibration, pressure, rpm, current, humidity, operating_hours, failure`

## Repository structure

```text
smart-industrial-pyspark-mlops/
├── api/main.py
├── data/raw/
├── data/processed/
├── data/features/
├── database/init.sql
├── grafana/provisioning/
├── models/
├── monitoring/prometheus.yml
├── pyspark/
│   ├── common.py
│   ├── generate_data.py
│   ├── etl.py
│   ├── train.py
│   └── predict.py
├── tests/test_pipeline.py
├── Dockerfile.api
├── Dockerfile.spark
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run on Windows PowerShell

### 1. Start infrastructure

```powershell
docker compose up -d postgres mlflow prometheus grafana
```

### 2. Build Spark and API images

```powershell
docker compose build
```

### 3. Use your existing industrial CSV

Copy your existing `machine_sensor_data.csv` into:

```text
data/raw/machine_sensor_data.csv
```

Or generate a test dataset:

```powershell
docker compose run --rm spark python /app/pyspark/generate_data.py
```

### 4. Run ETL

```powershell
docker compose run --rm spark python /app/pyspark/etl.py
```

### 5. Train Spark ML model

```powershell
docker compose run --rm spark python /app/pyspark/train.py
```

### 6. Generate PostgreSQL predictions

```powershell
docker compose run --rm spark python /app/pyspark/predict.py
```

### 7. Start API

```powershell
docker compose up -d api
```

## URLs

- FastAPI: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- MLflow: http://localhost:5000

Grafana default login is `admin` / `admin`.

## API test

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/predict -ContentType "application/json" -Body '{"temperature":85,"vibration":7.5,"pressure":112,"rpm":1800,"current":15,"humidity":72,"operating_hours":8000}'
```

## API endpoints

- `GET /`
- `GET /api/health`
- `GET /api/machines`
- `GET /api/summary`
- `GET /api/predictions`
- `GET /api/predictions?machine_id=M-001`
- `POST /api/predict`
- `GET /metrics`

## Complete pipeline

```powershell
docker compose up -d postgres mlflow prometheus grafana
docker compose build
docker compose run --rm spark python /app/pyspark/etl.py
docker compose run --rm spark python /app/pyspark/train.py
docker compose run --rm spark python /app/pyspark/predict.py
docker compose up -d api
```

## What this project demonstrates

- PySpark DataFrames and distributed processing
- Industrial sensor-data cleaning
- Feature engineering
- Parquet data storage
- Spark MLlib Random Forest classification
- ML evaluation with accuracy, F1 and ROC-AUC
- MLflow experiment tracking
- PostgreSQL persistence
- FastAPI serving
- Prometheus API metrics
- Grafana monitoring
- Dockerized reproducible execution
- Pytest project checks

## Future extension

The CSV source can later be replaced by OPC UA, MQTT, Kafka, PLC, SCADA or MES ingestion while retaining the downstream PySpark/ML/MLOps architecture.

Recommended GitHub repository name:

`smart-industrial-pyspark-mlops`
