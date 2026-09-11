import streamlit as st
import pandas as pd
from valuation_engine import StartupValuationModel, run_scenario_analysis

st.set_page_config(
    page_title="Startup Valuation Simulator",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Startup Valuation Simulator")
st.markdown("*Interactive financial valuation engine combining Discounted Cash Flow (DCF) and Revenue Multiple models built with Streamlit.*")
st.divider()

# Sidebar: Financial Assumptions
st.sidebar.header("📊 Financial Assumptions")

revenue = st.sidebar.number_input("Current Annual Revenue ($M):", min_value=0.5, max_value=500.0, value=10.0, step=1.0)
growth = st.sidebar.slider("Projected YoY Revenue Growth Rate (%):", min_value=10, max_value=150, value=50, step=5) / 100.0
margin = st.sidebar.slider("Target Free Cash Flow Margin (%):", min_value=5, max_value=50, value=20, step=1) / 100.0

st.sidebar.subheader("Valuation Parameters")
sector = st.sidebar.selectbox("Industry Sector:", [
    "SaaS / Enterprise Software", "AI / DeepTech", "FinTech / Payments",
    "Consumer Tech / E-Commerce", "Healthcare Tech"
])
discount_rate = st.sidebar.slider("Discount Rate / WACC (%):", min_value=8, max_value=25, value=12) / 100.0
terminal_growth = st.sidebar.slider("Terminal Perpetual Growth (%):", min_value=1, max_value=5, value=3) / 100.0

# Run Valuation Model
model = StartupValuationModel(
    current_revenue=revenue,
    growth_rate=growth,
    fcf_margin=margin,
    discount_rate=discount_rate,
    terminal_growth=terminal_growth
)
dcf_results = model.calculate_dcf_valuation(years=5)
multiples_results = model.calculate_multiples_valuation(sector=sector)

# Blended Valuation (60% DCF + 40% Multiple)
blended_val = round(0.6 * dcf_results['enterprise_value'] + 0.4 * multiples_results['valuation'], 2)

# Metric Summary Cards
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Estimated Enterprise Value", f"${blended_val}M", delta="Blended Valuation")
with m2:
    st.metric("DCF Valuation", f"${dcf_results['enterprise_value']}M", delta=f"PV of FCFs: ${dcf_results['pv_of_cash_flows']}M")
with m3:
    st.metric("Revenue Multiple Value", f"${multiples_results['valuation']}M", delta=f"{multiples_results['multiple']}x Revenue Multiple")
with m4:
    st.metric("5-Year Terminal Value", f"${dcf_results['terminal_value']}M", delta="Gordon Growth")

st.divider()

# Charts & Projection Table
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📈 5-Year Financial Cash Flow Projections")
    proj_df = dcf_results['projection_df']
    st.dataframe(proj_df, use_container_width=True)

with col_right:
    st.subheader("📊 Projected Revenue vs Free Cash Flow ($M)")
    chart_data = proj_df.set_index("Year")[["Projected Revenue ($M)", "Free Cash Flow ($M)"]]
    st.bar_chart(chart_data)

st.divider()

# Scenario Analysis Table (Bull / Base / Bear)
st.subheader("🎯 Scenario Analysis & Valuation Sensitivity")
scenario_df = run_scenario_analysis(revenue, growth, margin)
st.dataframe(scenario_df, use_container_width=True)

st.caption("Developed as part of Placement Portfolio | Stack: Python, Financial Modeling (DCF & Multiples), Streamlit")
