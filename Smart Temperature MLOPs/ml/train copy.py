import os
from pathlib import Path
import joblib
import pandas as pd
import psycopg
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from ml.features import FEATURES, build_features, make_target

DB = os.getenv("DATABASE_URL", "postgresql://mlops:mlops@localhost:5433/smartmlops")
MODEL = Path(os.getenv("MODEL_PATH", "models/temperature_model.joblib"))
REFERENCE = Path(os.getenv("REFERENCE_PATH", "models/reference.csv"))

def train():
    with psycopg.connect(DB) as conn:
        df = pd.read_sql(
            "SELECT timestamp, temperature FROM temperature_readings ORDER BY timestamp",
            conn,
        )
    if len(df) < 50:
        print(f"Need 50 readings; currently {len(df)}")
        return False

    df = build_features(df)
    X, y = df[FEATURES], make_target(df)
    stratify = y if y.nunique() == 2 else None

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=.2, random_state=42, stratify=stratify
    )
    model = RandomForestClassifier(
        n_estimators=200, max_depth=8, random_state=42, class_weight="balanced"
    )
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)

    MODEL.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": model,
        "features": FEATURES,
        "accuracy": float(accuracy_score(yte, pred)),
        "f1": float(f1_score(yte, pred, zero_division=0)),
    }
    joblib.dump(artifact, MODEL)
    df[["temperature"]].to_csv(REFERENCE, index=False)

    print("MODEL:", MODEL)
    print("accuracy:", artifact["accuracy"])
    print("f1:", artifact["f1"])
    return True

if __name__ == "__main__":
    train()
