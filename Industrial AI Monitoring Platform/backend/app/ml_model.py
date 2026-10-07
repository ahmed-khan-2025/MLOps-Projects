from pathlib import Path

import joblib
import numpy as np

from app.config import settings


_model = None


def load_model():
    global _model

    model_path = Path(settings.model_path)

    if not model_path.exists():
        return None

    _model = joblib.load(model_path)

    return _model


def get_model():
    global _model

    if _model is None:
        _model = load_model()

    return _model


def predict_failure(
    temperature: float,
    vibration: float,
    pressure: float,
    rpm: float,
    current: float,
    humidity: float,
):
    model = get_model()

    if model is None:
        raise RuntimeError("ML model has not been trained yet.")

    features = np.array(
        [
            [
                temperature,
                vibration,
                pressure,
                rpm,
                current,
                humidity,
            ]
        ]
    )

    probability = model.predict_proba(features)[0][1]

    if probability >= 0.7:
        status = "CRITICAL"
    elif probability >= 0.4:
        status = "WARNING"
    else:
        status = "NORMAL"

    return float(probability), status