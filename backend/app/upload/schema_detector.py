import pandas as pd


def detect_schema(df: pd.DataFrame):

    numeric_columns = []
    categorical_columns = []
    datetime_columns = []

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_columns.append(col)

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_columns.append(col)

        else:

            # Try datetime conversion
            try:
                pd.to_datetime(df[col])
                datetime_columns.append(col)

            except:
                categorical_columns.append(col)

    return {
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns
    }