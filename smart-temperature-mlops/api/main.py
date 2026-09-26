
import os
from pathlib import Path

import joblib
import pandas as pd
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from starlette.responses import Response

from ml.features import build_features


# ============================================================
# CONFIGURATION
# ============================================================

DB = os.getenv("DATABASE_URL")
MODEL = Path(os.getenv("MODEL_PATH"))


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Smart Temperature MLOps API",
    version="1.0.0",
)


# ============================================================
# PROMETHEUS METRICS
# ============================================================

prediction_counter = Counter(
    "ml_prediction_total",
    "Total ML predictions",
)

temperature_gauge = Gauge(
    "machine_temperature_celsius",
    "Latest machine temperature",
)

prediction_gauge = Gauge(
    "machine_overheat_prediction",
    "1=overheat, 0=normal",
)


# ============================================================
# REQUEST MODEL
# ============================================================

class Prediction(BaseModel):
    temperature: float


# ============================================================
# DATABASE
# ============================================================

def recent(n=10):
    with psycopg.connect(DB) as conn:
        return conn.execute(
            """
            SELECT timestamp, temperature
            FROM temperature_readings
            ORDER BY timestamp DESC
            LIMIT %s
            """,
            (n,),
        ).fetchall()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": MODEL.exists(),
    }


# ============================================================
# TEMPERATURE DATA
# ============================================================

@app.get("/api/temperature")
def temperatures(limit: int = 100):

    with psycopg.connect(DB) as conn:
        rows = conn.execute(
            """
            SELECT timestamp, temperature
            FROM temperature_readings
            ORDER BY timestamp DESC
            LIMIT %s
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "timestamp": t,
            "temperature": v,
        }
        for t, v in reversed(rows)
    ]


# ============================================================
# PREDICTION
# ============================================================

@app.post("/api/predict")
def predict(body: Prediction):

    if not MODEL.exists():
        raise HTTPException(
            status_code=503,
            detail="Model not trained yet",
        )

    artifact = joblib.load(MODEL)

    rows = recent(10)

    df = pd.DataFrame(
        {
            "temperature": [
                r[1] for r in reversed(rows)
            ] + [body.temperature]
        }
    )

    X = build_features(df).tail(1)[
        artifact["features"]
    ]

    pred = int(
        artifact["model"].predict(X)[0]
    )

    prob = float(
        artifact["model"].predict_proba(X)[0][1]
    )

    prediction_counter.inc()
    temperature_gauge.set(body.temperature)
    prediction_gauge.set(pred)

    return {
        "temperature": body.temperature,
        "prediction": (
            "overheat"
            if pred
            else "normal"
        ),
        "overheat_probability": round(
            prob,
            4,
        ),
        "model_accuracy": artifact["accuracy"],
        "model_f1": artifact["f1"],
    }


# ============================================================
# LATEST PREDICTION
# ============================================================

@app.get("/api/predictions")
def latest_prediction():

    rows = recent(1)

    if not rows:
        return {
            "message": "No readings yet"
        }

    timestamp, value = rows[0]

    return {
        "timestamp": timestamp,
        **predict(
            Prediction(
                temperature=value
            )
        ),
    }


# ============================================================
# PROMETHEUS METRICS
# ============================================================

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )



