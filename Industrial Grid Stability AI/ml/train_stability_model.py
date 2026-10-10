from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from ml.features import make_features


DATA_PATH = "ml/data/training_data.csv"
MODEL_PATH = "ml/models/stability_model.joblib"


def main():

    # --------------------------------------------------
    # 1. Load dataset
    # --------------------------------------------------

    df = pd.read_csv(DATA_PATH)

    X = make_features(df)
    y = df["stability_label"]

    print("Dataset:")
    print(f"Total samples: {len(df)}")
    print()

    print("Class distribution:")
    print(y.value_counts().sort_index())
    print()

    # --------------------------------------------------
    # 2. Train / validation / test split
    # --------------------------------------------------

    # First split:
    # 70% training
    # 30% temporary
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        stratify=y,
        random_state=42,
    )

    # Second split:
    # 15% validation
    # 15% test
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        stratify=y_temp,
        random_state=42,
    )

    print("Data split:")
    print(f"Training:   {len(X_train)}")
    print(f"Validation: {len(X_val)}")
    print(f"Test:       {len(X_test)}")
    print()

    # --------------------------------------------------
    # 3. Train model
    # --------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # --------------------------------------------------
    # 4. Validation evaluation
    # --------------------------------------------------

    validation_pred = model.predict(X_val)

    validation_accuracy = accuracy_score(
        y_val,
        validation_pred,
    )

    print("Validation accuracy:")
    print(validation_accuracy)
    print()

    # --------------------------------------------------
    # 5. Final test evaluation
    # --------------------------------------------------

    test_pred = model.predict(X_test)

    test_accuracy = accuracy_score(
        y_test,
        test_pred,
    )

    print("TEST RESULTS")
    print("============")
    print("Accuracy:", test_accuracy)
    print()

    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            test_pred,
        )
    )

    print()

    print("Classification Report:")
    print(
        classification_report(
            y_test,
            test_pred,
            target_names=[
                "STABLE",
                "WARNING",
                "UNSTABLE",
            ],
        )
    )

    # --------------------------------------------------
    # 6. Save model
    # --------------------------------------------------

    Path("ml/models").mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        {
            "model": model,
            "classes": {
                0: "STABLE",
                1: "WARNING",
                2: "UNSTABLE",
            },
            "features": list(X.columns),
        },
        MODEL_PATH,
    )

    print()
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()