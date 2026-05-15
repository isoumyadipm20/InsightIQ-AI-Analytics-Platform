from app.analytics.kpi_engine.base_kpi import BaseKPI


class AverageOrderValueKPI(BaseKPI):

    def compute(self, df):

        required = ["revenue", "orders"]

        if not all(col in df.columns for col in required):
            return None

        revenue = df["revenue"].sum()
        orders = df["orders"].sum()

        if orders == 0:
            return None

        aov = revenue / orders

        return round(aov, 2)