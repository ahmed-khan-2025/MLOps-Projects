from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

NUM_ROWS = 5000
NUM_MACHINES = 20

OUTPUT_PATH = Path("data/raw/machine_sensor_data.csv")

np.random.seed(42)


# ============================================================
# CREATE MACHINE SENSOR DATA
# ============================================================

def create_dataset():

    machine_ids = np.random.randint(
        1,
        NUM_MACHINES + 1,
        size=NUM_ROWS
    )

    timestamps = pd.date_range(
        start="2026-01-01",
        periods=NUM_ROWS,
        freq="15min"
    )

    temperature = np.random.normal(
        loc=65,
        scale=8,
        size=NUM_ROWS
    )

    vibration = np.random.normal(
        loc=2.5,
        scale=0.7,
        size=NUM_ROWS
    )

    pressure = np.random.normal(
        loc=6.5,
        scale=0.8,
        size=NUM_ROWS
    )

    rpm = np.random.normal(
        loc=1500,
        scale=150,
        size=NUM_ROWS
    )

    current = np.random.normal(
        loc=18,
        scale=3,
        size=NUM_ROWS
    )

    humidity = np.random.normal(
        loc=55,
        scale=10,
        size=NUM_ROWS
    )

    operating_hours = np.random.uniform(
        low=100,
        high=10000,
        size=NUM_ROWS
    )


    # ========================================================
    # KEEP SENSOR VALUES REALISTIC
    # ========================================================

    temperature = np.clip(
        temperature,
        40,
        100
    )

    vibration = np.clip(
        vibration,
        0.1,
        6
    )

    pressure = np.clip(
        pressure,
        3,
        10
    )

    rpm = np.clip(
        rpm,
        800,
        2200
    )

    current = np.clip(
        current,
        8,
        30
    )

    humidity = np.clip(
        humidity,
        20,
        90
    )


    # ========================================================
    # CREATE FAILURE CONDITION
    # ========================================================

    failure_probability = (
        0.01

        + np.where(
            temperature > 80,
            0.25,
            0
        )

        + np.where(
            vibration > 3.5,
            0.25,
            0
        )

        + np.where(
            pressure > 8,
            0.15,
            0
        )

        + np.where(
            current > 23,
            0.15,
            0
        )

        + np.where(
            operating_hours > 8000,
            0.15,
            0
        )
    )

    failure_probability = np.clip(
        failure_probability,
        0,
        0.95
    )

    failure = np.random.binomial(
        1,
        failure_probability
    )


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        {
            "machine_id": machine_ids,
            "timestamp": timestamps,
            "temperature": temperature.round(2),
            "vibration": vibration.round(2),
            "pressure": pressure.round(2),
            "rpm": rpm.round(2),
            "current": current.round(2),
            "humidity": humidity.round(2),
            "operating_hours": operating_hours.round(2),
            "failure": failure,
        }
    )


    # ========================================================
    # CREATE OUTPUT DIRECTORY
    # ========================================================

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # SAVE CSV
    # ========================================================

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("=" * 60)
    print("DATASET CREATED SUCCESSFULLY")
    print("=" * 60)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFailure distribution:")
    print(df["failure"].value_counts())

    print("\nFirst 10 rows:")
    print(df.head(10))


if __name__ == "__main__":
    create_dataset()