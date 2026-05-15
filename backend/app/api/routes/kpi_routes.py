from fastapi import APIRouter
import pandas as pd

from app.analytics.kpi_engine.registry import KPIRegistry

router = APIRouter()

DATA_PATH = "data/raw/sales.csv"


@router.get("/kpis")
def compute_kpis():

    df = pd.read_csv(DATA_PATH)

    results = KPIRegistry.compute_all(df)

    return {
        "kpis": results
    }