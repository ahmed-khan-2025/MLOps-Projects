import os
from pathlib import Path

import joblib
import pandas as pd
import psycopg
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from ml.features import FEATURES, build_features, make_target


# ============================================================
# CONFIGURATION
# ============================================================

DB = os.getenv("DATABASE_URL")
MODEL = Path(os.getenv("MODEL_PATH"))
REFERENCE = Path(os.getenv("REFERENCE_PATH"))


# ============================================================
# TRAIN MODEL
# ============================================================

def train():

    # --------------------------------------------------------
    # Load temperature data from PostgreSQL
    # --------------------------------------------------------

    with psycopg.connect(DB) as conn:
        df = pd.read_sql(
            """
            SELECT timestamp, temperature
            FROM temperature_readings
            ORDER BY timestamp
            """,
            conn,
        )

    # --------------------------------------------------------
    # Check minimum data
    # --------------------------------------------------------

    if len(df) < 50:
        print(
            f"Need 50 readings; currently {len(df)}"
        )
        return False

    # --------------------------------------------------------
    # Build features and target
    # --------------------------------------------------------

    df = build_features(df)

    X = df[FEATURES]
    y = make_target(df)

    # --------------------------------------------------------
    # Stratified split when both classes exist
    # --------------------------------------------------------

    stratify = (
        y
        if y.nunique() == 2
        else None
    )

    Xtr, Xte, ytr, yte = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(Xtr, ytr)

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    pred = model.predict(Xte)

    accuracy = accuracy_score(
        yte,
        pred,
    )

    f1 = f1_score(
        yte,
        pred,
        zero_division=0,
    )

    # --------------------------------------------------------
    # Create model directory
    # --------------------------------------------------------

    MODEL.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REFERENCE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Save model artifact
    # --------------------------------------------------------

    artifact = {
        "model": model,
        "features": FEATURES,
        "accuracy": float(accuracy),
        "f1": float(f1),
    }

    joblib.dump(
        artifact,
        MODEL,
    )

    # --------------------------------------------------------
    # Save reference data for drift detection
    # --------------------------------------------------------

    df[["temperature"]].to_csv(
        REFERENCE,
        index=False,
    )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    print("MODEL:", MODEL)
    print("REFERENCE:", REFERENCE)
    print("accuracy:", artifact["accuracy"])
    print("f1:", artifact["f1"])

    return True


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    train()

