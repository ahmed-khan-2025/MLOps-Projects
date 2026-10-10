
import pandas as pd

from ml.features import make_features, FEATURE_COLUMNS


def test_features():
    d = pd.DataFrame(
        [
            {
                "voltage": 0.95,
                "current": 150,
                "frequency": 49.5,
                "active_power": 90,
                "reactive_power": 40,
                "power_factor": 0.82,
                "voltage_angle": 4,
            }
        ]
    )

    x = make_features(d)

    assert list(x.columns) == FEATURE_COLUMNS
    assert x.shape == (1, 7)
    assert x.isna().sum().sum() == 0
