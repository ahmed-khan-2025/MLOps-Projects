import pandas as pd
from ml.features import build_features, make_target

def test_features():
    df = pd.DataFrame({"temperature": [50, 60, 80]})
    out = build_features(df)
    assert "rolling_mean" in out
    assert "rolling_std" in out

def test_target():
    df = pd.DataFrame({"temperature": [60, 70, 80]})
    assert make_target(df).tolist() == [0, 1, 1]
