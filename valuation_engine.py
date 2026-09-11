import numpy as np
import pandas as pd

class StartupValuationModel:
    """
    Financial valuation engine combining Discounted Cash Flow (DCF)
    and Industry Revenue Multiples for early-stage startup valuation.
    """
    def __init__(self, current_revenue, growth_rate, fcf_margin, discount_rate=0.12, terminal_growth=0.03):
        self.current_revenue = current_revenue
        self.growth_rate = growth_rate
        self.fcf_margin = fcf_margin
        self.discount_rate = discount_rate # WACC
        self.terminal_growth = terminal_growth

    def calculate_dcf_valuation(self, years=5):
        """Projects 5-year Free Cash Flows and computes Enterprise Valuation via DCF."""
        years_list = [f"Year {i}" for i in range(1, years + 1)]
        projected_revenues = []
        projected_fcfs = []
        discount_factors = []
        discounted_fcfs = []

        rev = self.current_revenue
        for i in range(1, years + 1):
            rev = rev * (1 + self.growth_rate * (0.9 ** (i - 1))) # Growth decelerates naturally
            fcf = rev * self.fcf_margin
            df = 1 / ((1 + self.discount_rate) ** i)
            d_fcf = fcf * df

            projected_revenues.append(round(rev, 2))
            projected_fcfs.append(round(fcf, 2))
            discount_factors.append(round(df, 3))
            discounted_fcfs.append(round(d_fcf, 2))

        # Terminal Value via Gordon Growth Model
        terminal_fcf = projected_fcfs[-1] * (1 + self.terminal_growth)
        terminal_value = terminal_fcf / (self.discount_rate - self.terminal_growth)
        discounted_tv = terminal_value / ((1 + self.discount_rate) ** years)

        enterprise_value = sum(discounted_fcfs) + discounted_tv

        projection_df = pd.DataFrame({
            "Year": years_list,
            "Projected Revenue ($M)": projected_revenues,
            "Free Cash Flow ($M)": projected_fcfs,
            "Discounted FCF ($M)": discounted_fcfs
        })

        return {
            "enterprise_value": round(enterprise_value, 2),
            "pv_of_cash_flows": round(sum(discounted_fcfs), 2),
            "discounted_terminal_value": round(discounted_tv, 2),
            "terminal_value": round(terminal_value, 2),
            "projection_df": projection_df
        }

    def calculate_multiples_valuation(self, sector="SaaS / Enterprise Software"):
        """Computes valuation based on industry revenue ARR multiples."""
        multiples = {
            "SaaS / Enterprise Software": 10.5,
            "FinTech / Payments": 8.0,
            "Consumer Tech / E-Commerce": 4.5,
            "AI / DeepTech": 14.0,
            "Healthcare Tech": 7.5
        }
        multiple = multiples.get(sector, 8.0)
        valuation = self.current_revenue * multiple
        return {
            "multiple": multiple,
            "valuation": round(valuation, 2)
        }

def run_scenario_analysis(current_revenue, base_growth, fcf_margin):
    """Generates Bear, Base, and Bull scenario valuations."""
    scenarios = {
        "Bear Case (-30% growth)": max(0.05, base_growth - 0.20),
        "Base Case (Expected)": base_growth,
        "Bull Case (+30% growth)": base_growth + 0.25
    }
    results = []
    for name, g in scenarios.items():
        model = StartupValuationModel(current_revenue, g, fcf_margin)
        dcf = model.calculate_dcf_valuation()
        mult = model.calculate_multiples_valuation()
        blended = round(0.6 * dcf['enterprise_value'] + 0.4 * mult['valuation'], 2)
        results.append({
            "Scenario": name,
            "Growth Rate": f"{int(g*100)}%",
            "DCF Value ($M)": f"${dcf['enterprise_value']}M",
            "Multiples Value ($M)": f"${mult['valuation']}M",
            "Blended Valuation ($M)": f"${blended}M"
        })
    return pd.DataFrame(results)

if __name__ == "__main__":
    model = StartupValuationModel(current_revenue=10.0, growth_rate=0.50, fcf_margin=0.20)
    dcf = model.calculate_dcf_valuation()
    print(f"DCF Enterprise Value: ${dcf['enterprise_value']}M")
    print(dcf['projection_df'])
