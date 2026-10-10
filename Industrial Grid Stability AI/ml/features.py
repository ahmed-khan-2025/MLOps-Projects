
import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "voltage_deviation",
    "frequency_deviation",
    "current_deviation",
    "power_factor_deviation",
    "reactive_power_ratio",
    "power_demand",
    "voltage_angle_abs",
]


def make_features(df):
    out = pd.DataFrame(index=df.index)

    out["voltage_deviation"] = (df["voltage"] - 1.0).abs()
    out["frequency_deviation"] = (df["frequency"] - 50.0).abs()
    out["current_deviation"] = (
        (df["current"] - 100.0) / 100.0
    ).abs()
    out["power_factor_deviation"] = (
        df["power_factor"] - 0.95
    ).abs()
    out["reactive_power_ratio"] = (
        df["reactive_power"].abs()
        / df["active_power"].abs().clip(lower=1.0)
    )
    out["power_demand"] = df["active_power"].abs()
    out["voltage_angle_abs"] = df["voltage_angle"].abs()

    return (
        out[FEATURE_COLUMNS]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
    )


def feature_row(m):
    return make_features(pd.DataFrame([m]))

