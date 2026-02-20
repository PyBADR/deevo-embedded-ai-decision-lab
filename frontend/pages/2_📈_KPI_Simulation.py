import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="KPI Simulation", page_icon="📈", layout="wide")

st.title("📈 KPI Simulation & ROI Calculator")

st.markdown("""
Simulate the business impact of the AI-driven decision intelligence system.
Adjust the parameters below to see projected cost savings and operational improvements.
""")

# Input sliders
col1, col2 = st.columns(2)

with col1:
    monthly_claims = st.slider("Monthly Claims Volume", 100, 10000, 1000, 100)
    avg_claim_cost = st.slider("Average Claim Amount (KWD)", 500, 50000, 5000, 500)

with col2:
    baseline_fraud_rate = st.slider("Baseline Fraud Rate (%)", 1.0, 20.0, 8.0, 0.5)
    detection_uplift = st.slider("AI Detection Uplift (%)", 0.0, 50.0, 15.0, 1.0)

# Calculations
st.subheader("📊 Projected Metrics")

# Fraud prevention
baseline_fraud_claims = monthly_claims * (baseline_fraud_rate / 100)
ai_fraud_detection = baseline_fraud_claims * (1 + detection_uplift / 100)
additional_fraud_caught = ai_fraud_detection - baseline_fraud_claims
fraud_savings = additional_fraud_caught * avg_claim_cost

# Auto-approval (assume 40% can be auto-approved)
auto_approved = monthly_claims * 0.40
manual_review_minutes = 12
time_saved_hours = (auto_approved * manual_review_minutes) / 60
labor_cost_per_hour = 25  # KWD
labor_savings = time_saved_hours * labor_cost_per_hour

# Total savings
total_monthly_savings = fraud_savings + labor_savings
annual_savings = total_monthly_savings * 12

# Display metrics
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Fraud Cases Detected", f"+{additional_fraud_caught:.0f}", f"{detection_uplift:.1f}% uplift")

with metric_col2:
    st.metric("Fraud Savings (Monthly)", f"{fraud_savings:,.0f} KWD", "prevented losses")

with metric_col3:
    st.metric("Time Saved (Monthly)", f"{time_saved_hours:,.0f} hours", "automation benefit")

with metric_col4:
    st.metric("Total Annual Savings", f"{annual_savings:,.0f} KWD", "combined ROI")

# ROI Breakdown Table
st.subheader("💰 ROI Breakdown")

roi_data = {
    "Category": ["Fraud Prevention", "Labor Cost Reduction", "Total"],
    "Monthly (KWD)": [
        f"{fraud_savings:,.0f}",
        f"{labor_savings:,.0f}",
        f"{total_monthly_savings:,.0f}"
    ],
    "Annual (KWD)": [
        f"{fraud_savings * 12:,.0f}",
        f"{labor_savings * 12:,.0f}",
        f"{annual_savings:,.0f}"
    ]
}

roi_df = pd.DataFrame(roi_data)
st.table(roi_df)

# Visualizations
st.subheader("📊 Visual Analysis")

col1, col2 = st.columns(2)

with col1:
    # Savings breakdown pie chart
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Fraud Prevention', 'Labor Reduction'],
        values=[fraud_savings, labor_savings],
        hole=0.3
    )])
    fig_pie.update_layout(title="Monthly Savings Breakdown")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Monthly projection
    months = list(range(1, 13))
    cumulative_savings = [total_monthly_savings * m for m in months]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months,
        y=cumulative_savings,
        mode='lines+markers',
        name='Cumulative Savings',
        line=dict(color='green', width=3)
    ))
    fig_line.update_layout(
        title="Cumulative Annual Savings",
        xaxis_title="Month",
        yaxis_title="Savings (KWD)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Business case
st.subheader("📋 Business Case Summary")

st.info(f"""
**Investment Case:**
- **Processing:** {monthly_claims:,} claims/month with {detection_uplift:.1f}% improved fraud detection
- **Efficiency:** {auto_approved:,.0f} claims auto-approved, saving {time_saved_hours:,.0f} hours
- **Financial Impact:** {annual_savings:,.0f} KWD annual savings
- **ROI Timeline:** Typically positive ROI within 3-6 months
""")
