import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Geographic Analysis", page_icon="🌍", layout="wide")

buyer_profile = load_data()

st.title("🌍 Geographic Buyer Analysis")
st.markdown("Analyze regional investment behavior, geographic concentration, and buyer distribution across countries and regions.")

# Sidebar filters
st.sidebar.header("Geographic Filters")

segments = ["All"] + sorted(buyer_profile["buyer_segment"].dropna().unique().tolist())
client_types = ["All"] + sorted(buyer_profile["client_type"].dropna().unique().tolist())

selected_segment = st.sidebar.selectbox("Buyer Segment", segments)
selected_client = st.sidebar.selectbox("Client Type", client_types)

filtered = buyer_profile.copy()

if selected_segment != "All":
    filtered = filtered[filtered["buyer_segment"] == selected_segment]

if selected_client != "All":
    filtered = filtered[filtered["client_type"] == selected_client]

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", filtered["country"].nunique())
col2.metric("Regions", filtered["region"].nunique())
col3.metric("Average Investment", f"${filtered['total_investment_value'].mean():,.0f}")
col4.metric("Average Satisfaction", f"{filtered['satisfaction_score'].mean():.2f}")

st.divider()

# Country distribution
st.subheader("Buyer Distribution by Country")

country_counts = (
    filtered["country"]
    .value_counts()
    .head(15)
    .reset_index()
)

country_counts.columns = ["Country", "Buyers"]

fig = px.bar(
    country_counts,
    x="Country",
    y="Buyers",
    color="Buyers",
    text="Buyers",
    title="Top Countries by Buyer Count"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Region distribution
st.subheader("Regional Buyer Distribution")

region_counts = (
    filtered["region"]
    .value_counts()
    .reset_index()
)

region_counts.columns = ["Region", "Buyers"]

fig = px.pie(
    region_counts,
    names="Region",
    values="Buyers",
    hole=0.45,
    title="Regional Distribution of Buyers"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Investment value by region
st.subheader("Average Investment Value by Region")

region_investment = (
    filtered
    .groupby("region")["total_investment_value"]
    .mean()
    .reset_index()
)

fig = px.bar(
    region_investment,
    x="region",
    y="total_investment_value",
    color="total_investment_value",
    text="total_investment_value",
    title="Average Investment Value by Region"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Geographic segment composition
st.subheader("Buyer Segments by Region")

region_segment = (
    filtered
    .groupby(["region", "buyer_segment"])
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    region_segment,
    x="region",
    y="Count",
    color="buyer_segment",
    barmode="stack",
    title="Buyer Segment Composition Across Regions"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Loan dependency by region
st.subheader("Loan Dependency by Region")

loan_region = (
    filtered
    .assign(loan_yes=filtered["loan_applied"].astype(str).str.lower().eq("yes").astype(int))
    .groupby("region")["loan_yes"]
    .mean()
    .reset_index()
)

loan_region["Loan Rate (%)"] = loan_region["loan_yes"] * 100

fig = px.bar(
    loan_region,
    x="region",
    y="Loan Rate (%)",
    color="Loan Rate (%)",
    text="Loan Rate (%)",
    title="Loan Application Rate by Region"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Satisfaction by region
st.subheader("Customer Satisfaction by Region")

fig = px.box(
    filtered,
    x="region",
    y="satisfaction_score",
    color="region",
    title="Satisfaction Distribution Across Regions"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Geographic investment summary
st.subheader("Regional Investment Summary")

regional_summary = filtered.groupby("region").agg(
    Buyers=("client_id", "count"),
    Average_Investment=("total_investment_value", "mean"),
    Average_Properties=("total_properties_owned", "mean"),
    Average_Satisfaction=("satisfaction_score", "mean")
).round(2)

st.dataframe(regional_summary, use_container_width=True)

st.divider()

# Executive insights
st.subheader("Geographic Investment Insights")

top_region = regional_summary["Average_Investment"].idxmax()
top_region_value = regional_summary.loc[top_region, "Average_Investment"]

largest_region = regional_summary["Buyers"].idxmax()
largest_region_buyers = regional_summary.loc[largest_region, "Buyers"]

st.markdown(f"""
### Executive Geographic Insights

- **Highest Investment Region:** {top_region}
- **Average Investment:** ${top_region_value:,.0f}
- **Largest Buyer Market:** {largest_region}
- **Buyer Count:** {largest_region_buyers}

These insights support regional expansion planning, premium property development, and geographically targeted marketing campaigns.
""")