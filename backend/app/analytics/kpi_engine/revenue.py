from app.analytics.kpi_engine.base_kpi import BaseKPI


class RevenueGrowthKPI(BaseKPI):

    def compute(self, df):

        if "revenue" not in df.columns:
            return None

        revenue = df["revenue"]

        if len(revenue) < 2:
            return None

        first = revenue.iloc[0]
        last = revenue.iloc[-1]

        growth = ((last - first) / first) * 100

        return round(growth, 2)