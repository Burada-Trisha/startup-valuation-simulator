# Startup Valuation Simulator

An interactive financial modeling application estimating early-stage startup enterprise valuations using **Discounted Cash Flow (DCF)** and **Industry Revenue Multiple** models built with the **Streamlit** framework.

## Key Features & Financial Models
- **Discounted Cash Flow (DCF):** Dynamic 5-year Free Cash Flow (FCF) projections discounted by Weighted Average Cost of Capital (WACC).
- **Terminal Value Modeling:** Evaluates perpetual exit valuations using the **Gordon Growth Model**.
- **Revenue Multiples:** Applies sector-specific ARR multiples across SaaS, FinTech, AI/DeepTech, and Consumer Tech.
- **Scenario Analysis:** Automated sensitivity comparison across **Bear Case**, **Base Case**, and **Bull Case** growth trajectories.
- **Interactive UI:** Streamlit dashboard featuring parameter sliders, real-time recalculations, cash flow bar charts, and projection data tables.

## Tech Stack
- **Languages:** Python
- **Financial Frameworks:** Discounted Cash Flow (DCF), Gordon Growth Terminal Value, Revenue ARR Multiples
- **Libraries:** Streamlit, Pandas, NumPy

## Financial Methodology Overview
1. **5-Year Cash Flow Projection:** Estimates revenue trajectory with natural deceleration factors and margin multipliers.
2. **Terminal Value Formula:**
   $$\text{Terminal Value} = \frac{\text{FCF}_5 \times (1 + g)}{r - g}$$
   *(where $r$ is the discount rate / WACC and $g$ is perpetual growth rate)*.
3. **Blended Valuation:** Combines intrinsic DCF valuation with market comparable revenue multiples for realistic valuation ranges.
