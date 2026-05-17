from fastapi import APIRouter
import pandas as pd

from app.anomaly_detection.anomaly_pipeline import (
    run_anomaly_pipeline
)

router = APIRouter()

DATA_PATH = "data/raw/sales.csv"


@router.get("/anomalies")
def detect_anomalies():

    df = pd.read_csv(DATA_PATH)

    results = run_anomaly_pipeline(df)

    return results