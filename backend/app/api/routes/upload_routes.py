from fastapi import APIRouter, UploadFile, File
import pandas as pd
import os

from app.upload.schema_detector import detect_schema
from app.upload.validator import validate_dataframe

router = APIRouter()

UPLOAD_DIR = "data/raw"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Read file
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file.filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)

    else:
        return {
            "error": "Unsupported file type"
        }

    # Schema detection
    schema_info = detect_schema(df)

    # Validation
    validation_info = validate_dataframe(df)

    return {

        "filename": file.filename,

        "dataset_shape": {
            "rows": df.shape[0],
            "columns": df.shape[1]
        },

        "schema": schema_info,

        "validation": validation_info,

        "preview": df.head(5).to_dict(orient="records")
    }