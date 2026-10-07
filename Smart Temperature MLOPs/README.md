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

## Data Flow

### OPC UA Server

The project starts a simulated industrial machine temperature source.

OPC UA node:

```text
ns=2;s=Machine.Temperature
```

The simulator generates continuously changing temperature values.

---

### Collector

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

### PostgreSQL

PostgreSQL stores the collected temperature history.

The Docker container uses:

```text
Database: smartmlops
User: mlops
Container port: 5432
Windows host port: 5433
```

---

### Machine Learning

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

## Model Evaluation

The training process uses:

```text
Train/Test split: 80/20
Random state: 42
```

The model reports:

* Accuracy
* F1 score

---

## FastAPI

The API provides machine-temperature prediction and monitoring endpoints.

### Health

```http
GET /api/health
```


### Temperature History

```http
GET /api/temperature
```

### Latest Prediction

```http
GET /api/predictions
```

### Prometheus Metrics

```http
GET /metrics
```

### Start everything

After the initial model has been trained:

```powershell
docker compose up -d
```
---

## Grafana

Open:

```text
http://localhost:3000
```
---

## Prometheus

Open:

```text
http://localhost:9090
```
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
