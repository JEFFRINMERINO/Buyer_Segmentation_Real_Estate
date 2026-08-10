import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from utils import load_data

st.set_page_config(page_title="Buyer Segmentation", page_icon="📊", layout="wide")

buyer_profile = load_data()

st.title("📊 Buyer Segmentation Analysis")
st.markdown("Explore AI-generated buyer segments and compare their investment characteristics.")

# Sidebar filters
st.sidebar.header("Segmentation Filters")

regions = ["All"] + sorted(buyer_profile["region"].dropna().unique().tolist())
client_types = ["All"] + sorted(buyer_profile["client_type"].dropna().unique().tolist())
purposes = ["All"] + sorted(buyer_profile["acquisition_purpose"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox("Region", regions)
selected_client = st.sidebar.selectbox("Client Type", client_types)
selected_purpose = st.sidebar.selectbox("Acquisition Purpose", purposes)

filtered = buyer_profile.copy()

if selected_region != "All":
    filtered = filtered[filtered["region"] == selected_region]

if selected_client != "All":
    filtered = filtered[filtered["client_type"] == selected_client]

if selected_purpose != "All":
    filtered = filtered[filtered["acquisition_purpose"] == selected_purpose]

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Buyer Segments", filtered["buyer_segment"].nunique())
col2.metric("Filtered Buyers", len(filtered))
col3.metric("Average Investment", f"${filtered['total_investment_value'].mean():,.0f}")

st.divider()

# Segment distribution
st.subheader("Segment Distribution")

segment_counts = (
    filtered["buyer_segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = ["Buyer Segment", "Buyers"]

fig = px.pie(
    segment_counts,
    names="Buyer Segment",
    values="Buyers",
    hole=0.45,
    title="Buyer Segment Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# PCA visualization
st.subheader("Buyer Segments in PCA Space")

pca_features = [
    "age",
    "satisfaction_score",
    "total_properties_owned",
    "total_investment_value",
    "average_property_value",
    "average_floor_area"
]

pca_data = filtered[pca_features].fillna(filtered[pca_features].median())

scaler = StandardScaler()
scaled = scaler.fit_transform(pca_data)

pca = PCA(n_components=2)
components = pca.fit_transform(scaled)

pca_df = pd.DataFrame({
    "PC1": components[:, 0],
    "PC2": components[:, 1],
    "Buyer Segment": filtered["buyer_segment"].values,
    "Investment Value": filtered["total_investment_value"].values
})

fig = px.scatter(
    pca_df,
    x="PC1",
    y="PC2",
    color="Buyer Segment",
    size="Investment Value",
    hover_data=["Investment Value"],
    title="PCA Visualization of Buyer Segments"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Segment comparison
st.subheader("Segment Comparison")

comparison = filtered.groupby("buyer_segment").agg(
    Buyers=("client_id", "count"),
    Avg_Age=("age", "mean"),
    Avg_Investment=("total_investment_value", "mean"),
    Avg_Properties=("total_properties_owned", "mean"),
    Avg_Satisfaction=("satisfaction_score", "mean")
).round(2)

st.dataframe(comparison, use_container_width=True)

st.divider()

# Investment by segment
st.subheader("Investment Distribution by Segment")

fig = px.box(
    filtered,
    x="buyer_segment",
    y="total_investment_value",
    color="buyer_segment",
    title="Investment Value by Buyer Segment"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Key insights
st.subheader("Key Segment Insights")

largest_segment = segment_counts.iloc[0]["Buyer Segment"]
largest_count = segment_counts.iloc[0]["Buyers"]

highest_investment = comparison["Avg_Investment"].idxmax()

st.markdown(f"""
### Executive Insights

- **Largest Segment:** {largest_segment} ({largest_count} buyers)
- **Highest Average Investment:** {highest_investment}
- **Number of Active Segments:** {comparison.shape[0]}
- **Filtered Buyer Population:** {len(filtered)}

These insights help identify high-value investor groups and prioritize targeted marketing strategies.
""")