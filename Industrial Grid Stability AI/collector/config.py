import os

from dotenv import load_dotenv


load_dotenv()


# ==========================================================
# PostgreSQL Configuration
# ==========================================================

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "gridai",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "griduser",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "gridpassword",
)

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = int(
    os.getenv(
        "POSTGRES_PORT",
        "5439",
    )
)


# ==========================================================
# TwinCAT ADS Configuration
# ==========================================================

PLC_AMS_NET_ID = os.getenv(
    "PLC_AMS_NET_ID",
    "199.4.42.250.1.1",
)

PLC_PORT = int(
    os.getenv(
        "PLC_PORT",
        "851",
    )
)


# ==========================================================
# Collector Configuration
# ==========================================================

MOCK_MODE = (
    os.getenv(
        "MOCK_MODE",
        "false",
    ).lower()
    == "true"
)

COLLECT_INTERVAL_SECONDS = float(
    os.getenv(
        "COLLECT_INTERVAL_SECONDS",
        "2",
    )
)


# ==========================================================
# ML Model Paths
# ==========================================================

STABILITY_MODEL_PATH = os.getenv(
    "STABILITY_MODEL_PATH",
    "ml/models/stability_model.joblib",
)

ANOMALY_MODEL_PATH = os.getenv(
    "ANOMALY_MODEL_PATH",
    "ml/models/anomaly_model.joblib",
)
