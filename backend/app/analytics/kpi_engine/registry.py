from app.analytics.kpi_engine.revenue import RevenueGrowthKPI
from app.analytics.kpi_engine.profit import ProfitMarginKPI
from app.analytics.kpi_engine.orders import AverageOrderValueKPI
from app.analytics.kpi_engine.efficiency import OperationalEfficiencyKPI


class KPIRegistry:

    KPIS = {
        "Revenue Growth %": RevenueGrowthKPI(),
        "Profit Margin %": ProfitMarginKPI(),
        "Average Order Value": AverageOrderValueKPI(),
        "Operational Efficiency %": OperationalEfficiencyKPI()
    }

    @classmethod
    def compute_all(cls, df):

        results = {}

        for name, kpi in cls.KPIS.items():

            try:
                results[name] = kpi.compute(df)

            except Exception:
                results[name] = None

        return results