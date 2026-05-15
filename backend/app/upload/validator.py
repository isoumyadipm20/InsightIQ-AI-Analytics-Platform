import pandas as pd


def validate_dataframe(df: pd.DataFrame):

    total_cells = df.shape[0] * df.shape[1]

    missing_values = df.isnull().sum().to_dict()

    total_missing = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()

    quality_score = round(
        ((total_cells - total_missing) / total_cells) * 100,
        2
    )

    return {
        "missing_values": missing_values,
        "total_missing": int(total_missing),
        "duplicate_rows": int(duplicate_rows),
        "quality_score": quality_score
    }