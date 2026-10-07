from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"


def generate_data(n_samples=5000):
    rng = np.random.default_rng(42)

    temperature = rng.normal(65, 12, n_samples)
    vibration = rng.normal(2.5, 0.8, n_samples)
    pressure = rng.normal(5, 0.6, n_samples)
    rpm = rng.normal(1500, 180, n_samples)
    current = rng.normal(8, 1.5, n_samples)
    humidity = rng.normal(50, 10, n_samples)

    failure_score = (
        (temperature > 80) * 2
        + (vibration > 3.5) * 2
        + (pressure > 6) * 1
        + (rpm > 1750) * 1
        + (current > 10) * 1
    )

    failure = (failure_score >= 2).astype(int)

    X = np.column_stack(
        [
            temperature,
            vibration,
            pressure,
            rpm,
            current,
            humidity,
        ]
    )

    return X, failure


def main():
    X, y = generate_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()