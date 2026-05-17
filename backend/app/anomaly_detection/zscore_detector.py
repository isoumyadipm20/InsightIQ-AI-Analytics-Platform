import pandas as pd
import numpy as np


def detect_zscore_anomalies(
    df: pd.DataFrame,
    column: str,
    threshold: float = 3
):

    mean = df[column].mean()
    std = df[column].std()

    z_scores = (df[column] - mean) / std

    anomalies = df[np.abs(z_scores) > threshold]

    return {
        "total_anomalies": len(anomalies),
        "anomaly_indices": anomalies.index.tolist(),
        "anomaly_records": anomalies.to_dict(orient="records")
    }