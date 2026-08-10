import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Investor Behavior", page_icon="💰", layout="wide")

buyer_profile = load_data()

st.title("💰 Investor Behavior Dashboard")
st.markdown("Analyze investment motivations, financing behavior, and customer acquisition channels.")

# Sidebar filters
st.sidebar.header("Behavior Filters")

segments = ["All"] + sorted(buyer_profile["buyer_segment"].dropna().unique().tolist())
regions = ["All"] + sorted(buyer_profile["region"].dropna().unique().tolist())

selected_segment = st.sidebar.selectbox("Buyer Segment", segments)
selected_region = st.sidebar.selectbox("Region", regions)

filtered = buyer_profile.copy()

if selected_segment != "All":
    filtered = filtered[filtered["buyer_segment"] == selected_segment]

if selected_region != "All":
    filtered = filtered[filtered["region"] == selected_region]

# KPIs
col1, col2, col3, col4 = st.columns(4)

investment_buyers = (
    filtered["acquisition_purpose"]
    .astype(str)
    .str.lower()
    .eq("investment")
    .sum()
)

loan_buyers = (
    filtered["loan_applied"]
    .astype(str)
    .str.lower()
    .eq("yes")
    .sum()
)

avg_investment = filtered["total_investment_value"].mean()
avg_properties = filtered["total_properties_owned"].mean()

col1.metric("Investment Buyers", f"{investment_buyers:,}")
col2.metric("Loan Applicants", f"{loan_buyers:,}")
col3.metric("Average Investment", f"${avg_investment:,.0f}")
col4.metric("Average Properties", f"{avg_properties:.2f}")

st.divider()

# Acquisition purpose
st.subheader("Acquisition Purpose Distribution")

purpose_counts = (
    filtered["acquisition_purpose"]
    .value_counts()
    .reset_index()
)

purpose_counts.columns = ["Purpose", "Buyers"]

fig = px.pie(
    purpose_counts,
    names="Purpose",
    values="Buyers",
    hole=0.45,
    title="Investment vs Personal Purchases"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Loan behavior
st.subheader("Loan Application Behavior")

loan_counts = (
    filtered["loan_applied"]
    .value_counts()
    .reset_index()
)

loan_counts.columns = ["Loan Applied", "Buyers"]

fig = px.bar(
    loan_counts,
    x="Loan Applied",
    y="Buyers",
    color="Loan Applied",
    text="Buyers",
    title="Loan Application Distribution"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Loan by segment
st.subheader("Loan Dependency by Buyer Segment")

loan_segment = (
    filtered
    .groupby(["buyer_segment", "loan_applied"])
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    loan_segment,
    x="buyer_segment",
    y="Count",
    color="loan_applied",
    barmode="group",
    title="Loan Dependency Across Buyer Segments"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Referral channels
st.subheader("Customer Acquisition Channels")

referral_counts = (
    filtered["referral_channel"]
    .value_counts()
    .reset_index()
)

referral_counts.columns = ["Referral Channel", "Buyers"]

fig = px.bar(
    referral_counts,
    x="Referral Channel",
    y="Buyers",
    color="Buyers",
    text="Buyers",
    title="Referral Channel Effectiveness"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Investment value by purpose
st.subheader("Investment Value by Acquisition Purpose")

fig = px.box(
    filtered,
    x="acquisition_purpose",
    y="total_investment_value",
    color="acquisition_purpose",
    title="Investment Value by Purchase Purpose"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Segment investment comparison
st.subheader("Segment Investment Comparison")

segment_investment = filtered.groupby("buyer_segment").agg(
    Average_Investment=("total_investment_value", "mean"),
    Average_Properties=("total_properties_owned", "mean"),
    Average_Satisfaction=("satisfaction_score", "mean")
).round(2)

st.dataframe(segment_investment, use_container_width=True)

st.divider()

# Strategic insights
st.subheader("Strategic Marketing Insights")

highest_investment_segment = segment_investment["Average_Investment"].idxmax()
highest_satisfaction_segment = segment_investment["Average_Satisfaction"].idxmax()

st.markdown(f"""
### Investor Behavior Insights

- **Highest Investment Segment:** {highest_investment_segment}
- **Highest Satisfaction Segment:** {highest_satisfaction_segment}
- **Total Investment-Oriented Buyers:** {investment_buyers}
- **Loan-Dependent Buyer Base:** {loan_buyers}

These insights help optimize financing offers, referral partnerships, and targeted investment marketing campaigns.
""")