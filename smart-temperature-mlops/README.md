# Smart Temperature MLOps

An end-to-end **Industrial AI / MLOps** project for machine-temperature monitoring, overheat prediction, data-drift detection, and automated model retraining.

The project simulates an industrial temperature sensor through **OPC UA**, collects the data into **PostgreSQL**, trains a machine-learning model, exposes predictions through **FastAPI**, monitors data drift, and visualizes operational metrics with **Prometheus and Grafana**.

---

## Architecture

```text
                    ┌──────────────────────┐
                    │   OPC UA Simulator   │
                    │  Machine.Temperature │
                    └──────────┬───────────┘
                               │
                               │ OPC UA
                               ▼
                    ┌──────────────────────┐
                    │      Collector       │
                    │     Python/asyncua   │
                    └──────────┬───────────┘
                               │
                               │ Temperature data
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │ temperature_readings │
                    └──────────┬───────────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                     ▼                   ▼
              ┌──────────────┐    ┌──────────────┐
              │    Trainer   │    │   Monitor    │
              │ RandomForest │    │  KS Drift    │
              └──────┬───────┘    └──────┬───────┘
                     │                   │
                     │ model.joblib      │ drift
                     ▼                   │
              ┌──────────────┐           │
              │    Models    │◄──────────┘
              │ .joblib/.csv │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   FastAPI    │
              │  Prediction  │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │  Prometheus  │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   Grafana    │
              └──────────────┘
```

---

## Project Goals

The project demonstrates a complete industrial machine-learning lifecycle:

* OPC UA industrial data acquisition
* Real-time temperature collection
* PostgreSQL data storage
* Feature engineering
* Machine-learning training
* Overheat classification
* Model persistence with Joblib
* FastAPI prediction API
* Data-drift detection
* Automated model retraining
* Prometheus monitoring
* Grafana visualization
* Docker containerization
* Environment-based configuration

---

## Technology Stack

| Area                     | Technology              |
| ------------------------ | ----------------------- |
| Programming              | Python 3.12             |
| Industrial Communication | OPC UA                  |
| OPC UA Library           | asyncua                 |
| Database                 | PostgreSQL 17           |
| Machine Learning         | scikit-learn            |
| Model                    | Random Forest           |
| Data Processing          | Pandas                  |
| Model Storage            | Joblib                  |
| API                      | FastAPI                 |
| API Server               | Uvicorn                 |
| Drift Detection          | Kolmogorov-Smirnov test |
| Monitoring               | Prometheus              |
| Visualization            | Grafana                 |
| Containers               | Docker / Docker Compose |
| Configuration            | `.env`                  |

---

## Project Structure

```text
smart-temperature-mlops/
│
├── api/
│   └── main.py
│
├── collector/
│   ├── collector.py
│   └── requirements.txt
│
├── ml/
│   ├── features.py
│   └── train.py
│
├── monitor/
│   └── monitor.py
│
├── opcua_server/
│   ├── server.py
│   └── requirements.txt
│
├── models/
│   ├── temperature_model.joblib
│   └── reference.csv
│
├── prometheus/
│   └── prometheus.yml
│
├── grafana/
│   └── provisioning/
│
├── Dockerfile.api
├── Dockerfile.collector
├── Dockerfile.monitor
├── Dockerfile.opcua
├── Dockerfile.trainer
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

## Data Flow

### 1. OPC UA Server

The project starts a simulated industrial machine temperature source.

OPC UA node:

```text
ns=2;s=Machine.Temperature
```

The simulator generates continuously changing temperature values.

---

### 2. Collector

The collector connects to the OPC UA server and reads the temperature every second.

Data is stored in PostgreSQL:

```text
temperature_readings
```

Table structure:

```text
id
timestamp
temperature
```

---

### 3. PostgreSQL

PostgreSQL stores the collected temperature history.

The Docker container uses:

```text
Database: smartmlops
User: mlops
Container port: 5432
Windows host port: 5433
```

---

### 4. Machine Learning

The trainer reads temperature data from PostgreSQL.

The project uses a:

```text
RandomForestClassifier
```

The model is trained to classify machine temperature conditions as:

```text
normal
overheat
```

The trained model is saved as:

```text
models/temperature_model.joblib
```

The reference temperature distribution used for drift detection is saved as:

```text
models/reference.csv
```

---

## Machine Learning Features

Feature engineering is performed using the temperature time series.

Features include temperature-based historical information used by the classifier.

The exact feature list is defined in:

```text
ml/features.py
```

---

## Model Evaluation

The training process uses:

```text
Train/Test split: 80/20
Random state: 42
```

The model reports:

* Accuracy
* F1 score

Example successful training output:

```text
MODEL: /app/models/temperature_model.joblib
REFERENCE: /app/models/reference.csv
accuracy: 1.0
f1: 1.0
```

The reported result is specific to the collected simulator dataset and should not be interpreted as a general real-world performance estimate.

---

## Data Drift Detection

The monitoring service continuously compares recent production temperature data against the reference distribution.

The project uses the:

```text
Kolmogorov-Smirnov (KS) test
```

Configuration:

```text
DRIFT_WINDOW=100
DRIFT_P_VALUE=0.01
```

Drift is detected when:

```text
p-value < 0.01
```

When drift is detected, the monitor can automatically trigger model retraining, subject to the configured cooldown period.

```text
RETRAIN_COOLDOWN_SECONDS=300
```

---

## FastAPI

The API provides machine-temperature prediction and monitoring endpoints.

### Health

```http
GET /api/health
```

Example:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### Temperature History

```http
GET /api/temperature
```

### Prediction

```http
POST /api/predict
```

Request:

```json
{
  "temperature": 45
}
```

Example response:

```json
{
  "temperature": 45,
  "prediction": "normal",
  "overheat_probability": 0.01,
  "model_accuracy": 1.0,
  "model_f1": 1.0
}
```

### Latest Prediction

```http
GET /api/predictions
```

### Prometheus Metrics

```http
GET /metrics
```

---

## Running the Project

### 1. Open the project

```powershell
cd "C:\Galib\ABC-Personal\4 Own Python Projects\Machine Learning projects\smart-temperature-mlops"
```

### 2. Validate Docker Compose

```powershell
docker compose config
```

### 3. Stop previous containers

```powershell
docker compose down
```

### 4. Build the images

```powershell
docker compose build
```

### 5. Start PostgreSQL and OPC UA

```powershell
docker compose up -d postgres opcua-server
```

### 6. Start the collector

```powershell
docker compose up -d collector
```

### 7. Train the model

Make sure PostgreSQL has at least 50 temperature readings.

```powershell
docker compose run --rm trainer
```

### 8. Start the API

```powershell
docker compose up -d api
```

### 9. Start monitoring

```powershell
docker compose up -d monitor prometheus grafana
```

### 10. Start everything

After the initial model has been trained:

```powershell
docker compose up -d
```

---

## Useful Commands

### Check containers

```powershell
docker compose ps
```

### Collector logs

```powershell
docker compose logs collector --tail 30
```

### OPC UA logs

```powershell
docker compose logs opcua-server --tail 30
```

### API logs

```powershell
docker compose logs api --tail 30
```

### Monitor logs

```powershell
docker compose logs monitor --tail 30
```

### Check database

```powershell
docker compose exec postgres psql -U mlops -d smartmlops
```

Then:

```sql
SELECT COUNT(*) FROM temperature_readings;
```

And:

```sql
SELECT *
FROM temperature_readings
ORDER BY timestamp DESC
LIMIT 10;
```

Exit PostgreSQL:

```sql
\q
```

---

## Services and Ports

| Service      | URL / Port                                   |
| ------------ | -------------------------------------------- |
| OPC UA       | `opc.tcp://localhost:4841/freeopcua/server/` |
| PostgreSQL   | `localhost:5433`                             |
| FastAPI      | `http://localhost:8000`                      |
| FastAPI Docs | `http://localhost:8000/docs`                 |
| Prometheus   | `http://localhost:9090`                      |
| Grafana      | `http://localhost:3000`                      |

---

## Grafana

Open:

```text
http://localhost:3000
```

Default credentials configured for this local project:

```text
Username: admin
Password: admin
```

Grafana can be used to visualize Prometheus metrics such as:

```text
machine_temperature_celsius
machine_overheat_prediction
ml_prediction_total
ml_data_drift_detected
ml_data_drift_p_value
ml_retraining_total
```

---

## Prometheus

Open:

```text
http://localhost:9090
```

Example metrics:

```text
machine_temperature_celsius
```

```text
machine_overheat_prediction
```

```text
ml_data_drift_detected
```

```text
ml_data_drift_p_value
```

```text
ml_retraining_total
```

---

## Environment Configuration

Configuration is stored in:

```text
.env
```

The `.env` file contains database, OPC UA, model, API, monitoring, Prometheus, and Grafana configuration.

Do not commit `.env` to GitHub because it contains credentials.

For a public repository, provide a safe example such as:

```text
.env.example
```

with placeholder values.

---

## Industrial Deployment Concept

The current OPC UA server is a **simulation** for development and testing.

The architecture can later be connected to real industrial equipment:

```text
Real Temperature Sensor
        ↓
PLC / Industrial Device
        ↓
OPC UA Server
        ↓
Collector
        ↓
PostgreSQL
        ↓
ML Model
        ↓
FastAPI
        ↓
Monitoring / Alerting
```

Possible future integrations include:

* PLC systems
* Industrial temperature sensors
* OPC UA-enabled machines
* SCADA systems
* MES systems
* MQTT
* Edge computing
* Industrial gateways

---

## MLOps Lifecycle

```text
Collect
   ↓
Store
   ↓
Prepare
   ↓
Train
   ↓
Evaluate
   ↓
Deploy
   ↓
Predict
   ↓
Monitor
   ↓
Detect Drift
   ↓
Retrain
   ↓
Deploy Updated Model
```

---

## Current Status

The prototype currently demonstrates:

* [x] OPC UA temperature simulation
* [x] OPC UA data collection
* [x] PostgreSQL storage
* [x] Feature engineering
* [x] Random Forest training
* [x] Model persistence
* [x] FastAPI prediction API
* [x] Prometheus metrics
* [x] Grafana monitoring
* [x] Data drift detection
* [x] Automated retraining
* [x] Docker Compose deployment
* [ ] Real physical temperature sensor
* [ ] PLC integration
* [ ] Production deployment

---

## Future Improvements

Potential extensions:

1. Connect a real industrial temperature sensor.
2. Connect the system to a PLC through OPC UA.
3. Add additional machine sensors such as vibration, pressure, current, and RPM.
4. Add time-series forecasting.
5. Add alert notifications for overheating.
6. Add model versioning.
7. Add MLflow experiment tracking.
8. Add CI/CD.
9. Add automated model validation before deployment.
10. Deploy the system to an industrial edge device or cloud environment.

---

## Author

**Ahmed Khan**

Software Developer | Python | Machine Learning | Industrial AI | MLOps

Sweden
