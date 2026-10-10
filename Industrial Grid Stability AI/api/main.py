from fastapi import FastAPI, HTTPException, Query
from prometheus_client import (
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from starlette.responses import Response

from api.database import (
    get_connection,
    fetch_latest_measurement,
    fetch_measurements,
    fetch_latest_prediction,
    fetch_predictions,
)


app = FastAPI(
    title="Industrial Grid Stability AI",
    version="1.0.0",
)


# ============================================================
# Prometheus Metrics
# ============================================================

grid_voltage = Gauge(
    "grid_voltage_pu",
    "Latest grid voltage",
)

grid_frequency = Gauge(
    "grid_frequency_hz",
    "Latest grid frequency",
)

grid_current = Gauge(
    "grid_current_a",
    "Latest grid current",
)

grid_active_power = Gauge(
    "grid_active_power_kw",
    "Latest grid active power",
)

grid_reactive_power = Gauge(
    "grid_reactive_power_kvar",
    "Latest grid reactive power",
)

grid_power_factor = Gauge(
    "grid_power_factor",
    "Latest grid power factor",
)

grid_stability_risk = Gauge(
    "grid_stability_risk_score",
    "Grid stability risk score from 0 to 100",
)

grid_stability_probability = Gauge(
    "grid_stability_probability",
    "Predicted stability-class probability",
)

grid_anomaly_score = Gauge(
    "grid_anomaly_score",
    "Anomaly severity score from 0 to 100",
)

grid_anomaly_detected = Gauge(
    "grid_anomaly_detected",
    "1 if anomaly is detected, otherwise 0",
)


# ============================================================
# Update Prometheus Metrics
# ============================================================

def update_metrics():
    """
    Update Prometheus metrics using the latest
    measurement and stability prediction.
    """

    measurement = fetch_latest_measurement()
    prediction = fetch_latest_prediction()

    if measurement:

        grid_voltage.set(
            measurement["voltage"]
        )

        grid_frequency.set(
            measurement["frequency"]
        )

        grid_current.set(
            measurement["current"]
        )

        grid_active_power.set(
            measurement["active_power"]
        )

        grid_reactive_power.set(
            measurement["reactive_power"]
        )

        grid_power_factor.set(
            measurement["power_factor"]
        )

    if prediction:

        grid_stability_risk.set(
            prediction["risk_score"]
        )

        grid_stability_probability.set(
            prediction["stability_probability"]
        )

        grid_anomaly_score.set(
            prediction["anomaly_score"]
        )

        grid_anomaly_detected.set(
            1
            if prediction["anomaly_status"] == "ANOMALY"
            else 0
        )


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():

    try:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute("SELECT 1")

        return {
            "status": "ok",
            "database": "ok",
        }

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )


# ============================================================
# Latest Measurement
# ============================================================

@app.get("/api/measurements/latest")
def latest_measurement():

    measurement = fetch_latest_measurement()

    if not measurement:

        raise HTTPException(
            status_code=404,
            detail="No measurements available",
        )

    return dict(measurement)


# ============================================================
# Measurement History
# ============================================================

@app.get("/api/measurements")
def measurements(
    limit: int = Query(
        100,
        ge=1,
        le=1000,
    )
):

    return [
        dict(row)
        for row in fetch_measurements(limit)
    ]


# ============================================================
# Latest Stability Prediction
# ============================================================

@app.get("/api/stability/latest")
def latest_stability():

    prediction = fetch_latest_prediction()

    if not prediction:

        raise HTTPException(
            status_code=404,
            detail="No stability predictions available",
        )

    update_metrics()

    return dict(prediction)


# ============================================================
# Stability Prediction History
# ============================================================

@app.get("/api/stability")
def stability(
    limit: int = Query(
        100,
        ge=1,
        le=1000,
    )
):

    return [
        dict(row)
        for row in fetch_predictions(limit)
    ]


# ============================================================
# Latest Anomaly
# ============================================================

@app.get("/api/anomalies/latest")
def latest_anomaly():

    prediction = fetch_latest_prediction()

    if not prediction:

        raise HTTPException(
            status_code=404,
            detail="No anomaly results available",
        )

    return {
        "timestamp": prediction["timestamp"],
        "anomaly_status": prediction["anomaly_status"],
        "anomaly_score": prediction["anomaly_score"],
        "risk_level": prediction["risk_level"],
    }


# ============================================================
# Prometheus Metrics
# ============================================================

@app.get("/metrics")
def metrics():

    update_metrics()

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
