import pandas as pd

from app.anomaly_detection.zscore_detector import (
    detect_zscore_anomalies
)

from app.anomaly_detection.isolation_forest_detector import (
    detect_isolation_forest
)

from app.anomaly_detection.risk_scoring import (
    compute_risk_score
)


def run_anomaly_pipeline(df: pd.DataFrame):

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if len(numeric_columns) == 0:

        return {
            "error": "No numeric columns found"
        }

    # Z-score detection

    primary_column = numeric_columns[0]

    zscore_results = detect_zscore_anomalies(
        df,
        primary_column
    )

    # Isolation Forest

    iso_results = detect_isolation_forest(
        df,
        numeric_columns
    )

    # Risk score

    risk_score = compute_risk_score(
        iso_results["total_anomalies"],
        len(df)
    )

    return {

        "zscore_detection": zscore_results,

        "isolation_forest_detection": iso_results,

        "risk_score": risk_score,

        "risk_level": (
            "HIGH"
            if risk_score > 20
            else "MODERATE"
            if risk_score > 5
            else "LOW"
        )
    }