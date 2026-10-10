from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

from ml.features import make_features


def main():

    # --------------------------------------------------
    # Load training data
    # --------------------------------------------------

    data_path = Path("ml/data/training_data.csv")

    df = pd.read_csv(data_path)

    print(f"Total samples: {len(df)}")

    print()
    print("Class distribution:")
    print(df["stability_label"].value_counts().sort_index())

    # --------------------------------------------------
    # Create ML features
    # --------------------------------------------------

    X = make_features(df)

    # --------------------------------------------------
    # Train anomaly detector only on STABLE data
    #
    # 0 = STABLE
    # 1 = WARNING
    # 2 = UNSTABLE
    # --------------------------------------------------

    stable_mask = df["stability_label"] == 0

    X_stable = X.loc[stable_mask]

    print()
    print(f"Stable samples used for anomaly training: {len(X_stable)}")

    # --------------------------------------------------
    # Isolation Forest
    # --------------------------------------------------

    model = IsolationForest(
        n_estimators=250,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_stable)

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    model_dir = Path("ml/models")
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "anomaly_model.joblib"

    joblib.dump(
        {
            "model": model,
            "features": list(X.columns),
        },
        model_path,
    )

    print()
    print(f"Anomaly model saved to: {model_path}")


if __name__ == "__main__":
    main()