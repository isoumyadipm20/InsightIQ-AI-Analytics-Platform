from fastapi import FastAPI

from app.api.routes import upload_routes
from app.api.routes import kpi_routes
from app.api.routes import anomaly_routes

app = FastAPI(
    title="InsightIQ",
    description="AI Powered KPI & Risk Intelligence Platform",
    version="1.0.0"
)

app.include_router(upload_routes.router)
app.include_router(kpi_routes.router)
app.include_router(anomaly_routes.router)

@app.get("/")
def root():
    return {
        "message": "InsightIQ Backend Running"
    }