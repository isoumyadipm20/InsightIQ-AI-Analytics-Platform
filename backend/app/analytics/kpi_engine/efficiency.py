from app.analytics.kpi_engine.base_kpi import BaseKPI


class OperationalEfficiencyKPI(BaseKPI):

    def compute(self, df):

        required = ["output", "input"]

        if not all(col in df.columns for col in required):
            return None

        output_total = df["output"].sum()
        input_total = df["input"].sum()

        if input_total == 0:
            return None

        efficiency = (output_total / input_total) * 100

        return round(efficiency, 2)