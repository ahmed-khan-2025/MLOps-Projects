FEATURES = ["temperature", "rolling_mean", "rolling_std"]

def build_features(df):
    result = df.copy()
    result["rolling_mean"] = result["temperature"].rolling(10, min_periods=1).mean()
    result["rolling_std"] = result["temperature"].rolling(10, min_periods=1).std().fillna(0)
    return result

def make_target(df):
    return (df["temperature"] >= 70).astype(int)
