from sklearn.ensemble import IsolationForest
import pandas as pd


def detect_isolation_forest(
    df: pd.DataFrame,
    columns: list
):

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    subset = df[columns]

    predictions = model.fit_predict(subset)

    df["anomaly"] = predictions

    anomalies = df[df["anomaly"] == -1]

    return {
        "total_anomalies": len(anomalies),
        "anomaly_records": anomalies.to_dict(orient="records")
    }