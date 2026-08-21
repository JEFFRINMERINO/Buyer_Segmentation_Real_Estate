import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from utils import load_data

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

buyer_profile = load_data()

from utils import PROJECT_ROOT

MODEL_DIR = PROJECT_ROOT / "models"

kmeans_path = MODEL_DIR / "kmeans_model.pkl"

kmeans = joblib.load(kmeans_path)

# Feature columns
feature_cols = [
    "age",
    "satisfaction_score",
    "total_properties_owned",
    "total_investment_value",
    "average_property_value",
    "average_floor_area"
]

X = buyer_profile[feature_cols].fillna(buyer_profile[feature_cols].median())

# PCA
pca = PCA(n_components=2)
components = pca.fit_transform(X)

clusters = buyer_profile["cluster"]

# Metrics
silhouette = silhouette_score(X, clusters)
davies = davies_bouldin_score(X, clusters)
calinski = calinski_harabasz_score(X, clusters)

st.title("📈 Clustering Model Performance")
st.markdown("Evaluation metrics and model quality analysis for the buyer segmentation system.")

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Clusters", clusters.nunique())
col2.metric("Silhouette Score", f"{silhouette:.3f}")
col3.metric("Davies-Bouldin", f"{davies:.3f}")
col4.metric("Calinski-Harabasz", f"{calinski:.0f}")

st.divider()

# Cluster distribution
st.subheader("Cluster Distribution")

cluster_counts = (
    buyer_profile["buyer_segment"]
    .value_counts()
    .reset_index()
)

cluster_counts.columns = ["Buyer Segment", "Buyers"]

fig = px.bar(
    cluster_counts,
    x="Buyer Segment",
    y="Buyers",
    color="Buyer Segment",
    text="Buyers",
    title="Distribution of Buyers Across Clusters"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# PCA explained variance
st.subheader("PCA Explained Variance")

variance_df = pd.DataFrame({
    "Component": ["PC1", "PC2"],
    "Explained Variance": pca.explained_variance_ratio_ * 100
})

fig = px.bar(
    variance_df,
    x="Component",
    y="Explained Variance",
    color="Component",
    text="Explained Variance",
    title="Variance Explained by Principal Components"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# PCA visualization
st.subheader("PCA Cluster Visualization")

pca_df = pd.DataFrame({
    "PC1": components[:, 0],
    "PC2": components[:, 1],
    "Buyer Segment": buyer_profile["buyer_segment"]
})

fig = px.scatter(
    pca_df,
    x="PC1",
    y="PC2",
    color="Buyer Segment",
    title="Cluster Separation in PCA Space",
    opacity=0.8
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Feature variability
st.subheader("Feature Variability Analysis")

feature_variance = (
    X.var()
    .sort_values(ascending=False)
    .reset_index()
)

feature_variance.columns = ["Feature", "Variance"]

fig = px.bar(
    feature_variance,
    x="Feature",
    y="Variance",
    color="Variance",
    title="Feature Variance Contribution"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Evaluation table
st.subheader("Clustering Evaluation Summary")

evaluation = pd.DataFrame({
    "Metric": [
        "Silhouette Score",
        "Davies-Bouldin Index",
        "Calinski-Harabasz Score"
    ],
    "Value": [
        round(silhouette, 4),
        round(davies, 4),
        round(calinski, 2)
    ]
})

st.dataframe(evaluation, use_container_width=True)

st.divider()

# Interpretation
st.subheader("Model Interpretation")

st.markdown(
    f"""
### Clustering Quality Assessment

- **Silhouette Score:** {silhouette:.3f}
- **Davies-Bouldin Index:** {davies:.3f}
- **Calinski-Harabasz Score:** {calinski:.0f}

The buyer segmentation model demonstrates measurable separation between clusters and provides a meaningful structure for identifying investment-oriented buyer groups.

These metrics validate the effectiveness of the clustering approach for real estate market intelligence and customer segmentation.
"""
)