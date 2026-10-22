import pandas as pd
from sklearn.ensemble import IsolationForest


def add_anomaly_predictions(logs):
    data = logs.copy()

    if data.empty:
        data["anomaly"] = pd.Series(dtype="object")
        return data

    data["failed"] = (data["status"] == "failed").astype(int)

    features = data.groupby("ip_address").agg(
        total_events=("status", "size"),
        failed_attempts=("failed", "sum"),
        unique_users=("username", "nunique")
    )

    if len(features) < 3:
        data["anomaly"] = "Insufficient data"
        return data

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )

    predictions = model.fit_predict(
        features[
            ["total_events", "failed_attempts", "unique_users"]
        ]
    )

    features["anomaly"] = [
        "Normal" if prediction == 1 else "Anomaly"
        for prediction in predictions
    ]

    data["anomaly"] = data["ip_address"].map(
        features["anomaly"]
    )

    return data