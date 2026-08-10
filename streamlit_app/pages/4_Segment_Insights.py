import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Segment Insights", page_icon="🧠", layout="wide")

buyer_profile = load_data()

st.title("🧠 Buyer Segment Insights")
st.markdown("Executive insights and strategic recommendations for each AI-generated buyer segment.")

# Sidebar filter
st.sidebar.header("Insight Filters")

segments = sorted(buyer_profile["buyer_segment"].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("Select Buyer Segment", segments)

segment_data = buyer_profile[buyer_profile["buyer_segment"] == selected_segment]

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Buyers", len(segment_data))
col2.metric("Average Investment", f"${segment_data['total_investment_value'].mean():,.0f}")
col3.metric("Average Properties", f"{segment_data['total_properties_owned'].mean():.2f}")
col4.metric("Average Satisfaction", f"{segment_data['satisfaction_score'].mean():.2f}")

st.divider()

# Segment profile
st.subheader(f"Segment Profile: {selected_segment}")

profile = segment_data.agg({
    "age": "mean",
    "satisfaction_score": "mean",
    "total_properties_owned": "mean",
    "total_investment_value": "mean",
    "average_property_value": "mean",
    "average_floor_area": "mean"
}).round(2)

profile_df = profile.reset_index()
profile_df.columns = ["Metric", "Value"]

st.dataframe(profile_df, use_container_width=True)

st.divider()

# Radar-style comparison (normalized values)
st.subheader("Segment Performance Overview")

comparison = buyer_profile.groupby("buyer_segment").agg({
    "age": "mean",
    "satisfaction_score": "mean",
    "total_properties_owned": "mean",
    "total_investment_value": "mean",
    "average_property_value": "mean"
})

normalized = (comparison - comparison.min()) / (comparison.max() - comparison.min())
selected_values = normalized.loc[selected_segment]

radar_df = pd.DataFrame({
    "Metric": selected_values.index,
    "Score": selected_values.values
})

fig = px.line_polar(
    radar_df,
    r="Score",
    theta="Metric",
    line_close=True,
    title=f"Normalized Performance Profile: {selected_segment}"
)

fig.update_traces(fill="toself")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Geographic concentration
st.subheader("Geographic Concentration")

region_counts = (
    segment_data["region"]
    .value_counts()
    .reset_index()
)

region_counts.columns = ["Region", "Buyers"]

fig = px.bar(
    region_counts,
    x="Region",
    y="Buyers",
    color="Buyers",
    text="Buyers",
    title=f"Regional Distribution: {selected_segment}"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Financing profile
st.subheader("Financing Profile")

loan_counts = (
    segment_data["loan_applied"]
    .value_counts()
    .reset_index()
)

loan_counts.columns = ["Loan Applied", "Buyers"]

fig = px.pie(
    loan_counts,
    names="Loan Applied",
    values="Buyers",
    hole=0.45,
    title=f"Loan Application Behavior: {selected_segment}"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Acquisition purpose
st.subheader("Investment Motivation")

purpose_counts = (
    segment_data["acquisition_purpose"]
    .value_counts()
    .reset_index()
)

purpose_counts.columns = ["Purpose", "Buyers"]

fig = px.bar(
    purpose_counts,
    x="Purpose",
    y="Buyers",
    color="Purpose",
    text="Buyers",
    title=f"Acquisition Purpose: {selected_segment}"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Strategic recommendations
st.subheader("Strategic Recommendations")

recommendations = {
    "First-Time Buyers": [
        "Promote affordable housing projects",
        "Offer EMI and financing assistance",
        "Use digital marketing campaigns"
    ],
    "Corporate Investors": [
        "Offer commercial property portfolios",
        "Provide dedicated relationship managers",
        "Develop enterprise investment packages"
    ],
    "Global Investors": [
        "Target premium international properties",
        "Provide cross-border investment support",
        "Focus on wealth preservation products"
    ],
    "Luxury Investors": [
        "Offer exclusive property previews",
        "Develop premium concierge services",
        "Prioritize luxury residential projects"
    ],
    "Diversified Investors": [
        "Promote mixed-use investment portfolios",
        "Offer portfolio diversification strategies",
        "Provide personalized investment advisory"
    ]
}

for rec in recommendations.get(selected_segment, []):
    st.markdown(f"- {rec}")

st.divider()

# Downloadable summary
st.subheader("Download Segment Summary")

download_df = segment_data[["client_id", "buyer_segment", "country", "region", "total_investment_value", "total_properties_owned", "satisfaction_score"]]

csv = download_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Segment CSV",
    data=csv,
    file_name=f"{selected_segment.lower().replace(' ', '_')}_summary.csv",
    mime="text/csv"
)

st.divider()

# Executive summary
st.subheader("Executive Summary")

st.markdown(f"""
### {selected_segment}

This segment contains **{len(segment_data)} buyers** with an average investment value of **${segment_data['total_investment_value'].mean():,.0f}**.

The segment demonstrates distinct geographic, financing, and investment characteristics that support targeted marketing, financing optimization, and premium property recommendation strategies.

This profile can be used by Parcl to improve customer targeting and investment intelligence.
""")