# MLOps-Projects

A collection of **Machine Learning Operations (MLOps), Industrial AI, ML monitoring, model deployment, data engineering, and production ML systems** projects.

These projects demonstrate the development and operation of machine learning systems across the complete ML lifecycle — from data collection and preprocessing to model training, deployment, monitoring, drift detection, and retraining.

## Projects

### 1. Smart Temperature MLOps

An end-to-end industrial MLOps platform that simulates machine temperature data and processes it through an industrial data pipeline.

The system connects simulated industrial data with **OPC UA, PostgreSQL, machine learning, FastAPI, Prometheus, Grafana, drift detection, and automated model retraining**.

**Focus:** Industrial IoT, OPC UA, Python, PostgreSQL, ML pipelines, FastAPI, Docker, Prometheus, Grafana, data drift, model retraining, and MLOps.

**Pipeline:**

```text
Temperature Simulation
        ↓
OPC UA
        ↓
Data Collector
        ↓
PostgreSQL
        ↓
Machine Learning
        ↓
FastAPI
        ↓
Prometheus
        ↓
Grafana
        ↓
Drift Detection
        ↓
Model Retraining
```

---

### 2. Smart Industrial PySpark MLOps

A distributed industrial machine learning pipeline using **Apache Spark, PostgreSQL, MLflow, FastAPI, Docker, and Grafana**.

The project demonstrates how industrial sensor data can be processed at scale, transformed into ML features, used for model training, tracked with MLflow, and exposed through an API.

**Focus:** Apache Spark, PySpark, ETL, feature engineering, Random Forest, MLflow, PostgreSQL, FastAPI, Docker, and ML monitoring.

**Industrial features include:**

* Temperature
* Vibration
* Pressure
* RPM
* Current
* Humidity
* Operating hours

**Pipeline:**

```text
Industrial Sensor Data
        ↓
PostgreSQL
        ↓
PySpark ETL
        ↓
Feature Engineering
        ↓
Machine Learning
        ↓
MLflow
        ↓
FastAPI
        ↓
Grafana
```

---

### 3. Industrial AI Monitoring Platform

An industrial machine monitoring platform that combines **machine learning predictions, backend APIs, database persistence, and real-time visualization**.

The platform provides machine readings and failure-probability information through a FastAPI backend and displays monitoring information through a React-based frontend.

**Focus:** Industrial AI, predictive monitoring, machine failure prediction, FastAPI, PostgreSQL, React, Docker, and ML-powered monitoring.

**Architecture:**

```text
Industrial Machine Data
        ↓
ML Prediction
        ↓
FastAPI
        ↓
PostgreSQL
        ↓
React Dashboard
        ↓
Industrial Monitoring
```

---

## Project Progression

The projects progressively explore different areas of production machine learning:

```text
Smart Temperature MLOps
        ↓
Smart Industrial PySpark MLOps
        ↓
Industrial AI Monitoring Platform
```

The progression covers:

```text
ML Pipeline Development
        ↓
Industrial Data Collection
        ↓
Data Engineering
        ↓
Feature Engineering
        ↓
Machine Learning
        ↓
Model Deployment
        ↓
ML Experiment Tracking
        ↓
Monitoring
        ↓
Data Drift Detection
        ↓
Model Retraining
        ↓
Industrial AI Systems
```

---
## Technology Stack

### Machine Learning

* Python
* scikit-learn
* Random Forest
* Feature Engineering
* Model Evaluation
* Model Retraining

### MLOps

* MLflow
* Prometheus
* Grafana
* Docker
* Model Monitoring
* Data Drift Detection
* Automated Retraining

### Data Engineering

* Apache Spark
* PySpark
* PostgreSQL
* ETL Pipelines
* Industrial Sensor Data

### Industrial AI

* OPC UA
* Industrial IoT
* Machine Monitoring
* Predictive Analytics
* Machine Failure Prediction

### Backend

* FastAPI
* REST APIs
* Python

### Frontend

* React
* Vite
* Recharts

---

## Repository Structure

Each project is maintained as an independent project with its own implementation, documentation, configuration, and deployment setup.

```text
MLOps-Projects/
│
├── README.md
│
├── smart-temperature-mlops/
│
├── smart-industrial-pyspark-mlops/
│
└── industrial-ai-monitoring-platform/
```

The individual projects can also be maintained as standalone GitHub repositories.

---

## MLOps Lifecycle

These projects demonstrate different stages of the production ML lifecycle:

```text
Data Collection
      ↓
Data Storage
      ↓
Data Processing
      ↓
Feature Engineering
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Model Deployment
      ↓
Monitoring
      ↓
Drift Detection
      ↓
Retraining
      ↓
Continuous ML Improvement
```

---

## MLOps vs LLM/RAG Projects

This repository focuses specifically on **machine learning operations and production ML systems**.

The LLM, RAG, agentic AI, MCP, and AI evaluation projects are maintained separately in:

**LLM-RAG-Projects**

```text
MLOps-Projects
│
├── Machine Learning
├── ML Pipelines
├── Data Engineering
├── Model Deployment
├── Monitoring
├── Drift Detection
├── Retraining
└── Industrial AI


LLM-RAG-Projects
│
├── LLMs
├── RAG
├── Multimodal AI
├── AI Agents
├── MCP
├── AI Evaluation
└── LLM Platforms
```

This separation keeps the portfolio clear and avoids presenting the same project in multiple categories.

---

## Portfolio Focus

These projects demonstrate practical experience in:

* Machine Learning Engineering
* MLOps
* Industrial AI
* Python
* Data Engineering
* ML Deployment
* ML Monitoring
* Model Lifecycle Management
* Industrial IoT
* Production ML Systems

They are designed to demonstrate not only how to **train machine learning models**, but also how to **deploy, monitor, maintain, and operate ML systems in production-oriented environments**.

---

## Author

**Ahmed Khan**

Machine Learning Engineer | Python | MLOps | Industrial AI

Stockholm, Sweden
