from app.analytics.kpi_engine.base_kpi import BaseKPI


class ProfitMarginKPI(BaseKPI):

    def compute(self, df):

        required = ["profit", "revenue"]

        if not all(col in df.columns for col in required):
            return None

        total_profit = df["profit"].sum()
        total_revenue = df["revenue"].sum()

        if total_revenue == 0:
            return None

        margin = (total_profit / total_revenue) * 100

        return round(margin, 2)