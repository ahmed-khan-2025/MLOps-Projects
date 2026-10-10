from pathlib import Path

import numpy as np
import pandas as pd


R = np.random.default_rng(42)


def gen(label, n):
    """
    Generate synthetic industrial grid stability data.

    0 = STABLE
    1 = WARNING
    2 = UNSTABLE
    """

    # --------------------------------------------------
    # Base operating point
    # --------------------------------------------------

    voltage = R.normal(1.0, 0.015, n)
    frequency = R.normal(50.0, 0.12, n)
    current = R.normal(100.0, 8.0, n)
    active_power = R.normal(70.0, 6.0, n)
    reactive_power = R.normal(20.0, 4.0, n)
    power_factor = np.clip(
        R.normal(0.95, 0.015, n),
        0.85,
        1.0,
    )
    voltage_angle = R.normal(0.0, 1.0, n)

    # --------------------------------------------------
    # Class-specific operating conditions
    # --------------------------------------------------

    if label == 0:

        # STABLE
        voltage += R.normal(0.015, 0.010, n)
        frequency += R.normal(0.03, 0.06, n)
        current += R.normal(0, 5, n)
        active_power += R.normal(0, 4, n)
        reactive_power += R.normal(0, 3, n)
        power_factor += R.normal(0.015, 0.010, n)
        voltage_angle += R.normal(0, 0.5, n)

    elif label == 1:

        # WARNING
        voltage += R.normal(-0.015, 0.012, n)
        frequency += R.normal(-0.08, 0.08, n)
        current += R.normal(15, 7, n)
        active_power += R.normal(8, 5, n)
        reactive_power += R.normal(7, 4, n)
        power_factor += R.normal(-0.035, 0.015, n)
        voltage_angle += R.normal(3, 1.0, n)

    else:

        # UNSTABLE
        voltage += R.normal(-0.040, 0.015, n)
        frequency += R.normal(-0.20, 0.10, n)
        current += R.normal(28, 9, n)
        active_power += R.normal(15, 6, n)
        reactive_power += R.normal(12, 5, n)
        power_factor += R.normal(-0.065, 0.020, n)
        voltage_angle += R.normal(6, 1.5, n)

    # --------------------------------------------------
    # Measurement noise
    # --------------------------------------------------

    voltage += R.normal(0, 0.006, n)
    frequency += R.normal(0, 0.035, n)
    current += R.normal(0, 2.5, n)
    active_power += R.normal(0, 2.0, n)
    reactive_power += R.normal(0, 1.5, n)
    power_factor += R.normal(0, 0.006, n)
    voltage_angle += R.normal(0, 0.35, n)

    # --------------------------------------------------
    # Physical limits
    # --------------------------------------------------

    voltage = np.clip(voltage, 0.85, 1.10)

    frequency = np.clip(
        frequency,
        48.0,
        52.0,
    )

    current = np.clip(
        current,
        50,
        160,
    )

    active_power = np.clip(
        active_power,
        30,
        120,
    )

    reactive_power = np.clip(
        reactive_power,
        5,
        60,
    )

    power_factor = np.clip(
        power_factor,
        0.70,
        1.0,
    )

    voltage_angle = np.clip(
        voltage_angle,
        -5,
        12,
    )

    return pd.DataFrame(
        {
            "voltage": voltage,
            "current": current,
            "frequency": frequency,
            "active_power": active_power,
            "reactive_power": reactive_power,
            "power_factor": power_factor,
            "voltage_angle": voltage_angle,
            "stability_label": label,
        }
    )


def main():

    stable = gen(0, 3000)
    warning = gen(1, 3000)
    unstable = gen(2, 3000)

    df = pd.concat(
        [
            stable,
            warning,
            unstable,
        ],
        ignore_index=True,
    )

    # Shuffle the dataset
    df = df.sample(
        frac=1,
        random_state=42,
    ).reset_index(drop=True)

    output_dir = Path("ml/data")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir /
        "training_data.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Generated {len(df)} samples"
    )

    print(
        f"Saved to: {output_file}"
    )

    print()

    print(
        "Class distribution:"
    )

    print(
        df["stability_label"]
        .value_counts()
        .sort_index()
    )


if __name__ == "__main__":
    main()