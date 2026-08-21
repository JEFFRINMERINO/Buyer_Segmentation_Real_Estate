import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

from utils import PROJECT_ROOT, load_data
st.set_page_config(
    page_title="Predict Buyer Segment",
    page_icon="🤖",
    layout="wide"
)

# Load historical data
buyer_profile = load_data()

MODEL_DIR = PROJECT_ROOT / "models"

kmeans_path = MODEL_DIR / "kmeans_model.pkl"
scaler_path = MODEL_DIR / "scaler.pkl"

kmeans = joblib.load(kmeans_path)
scaler = joblib.load(scaler_path)

st.title("🤖 Predict New Buyer Segment")
st.markdown(
    "Enter a new buyer profile and predict the most likely investment segment using the trained clustering model."
)

st.divider()

st.subheader("Buyer profile input")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 80, 35)
    satisfaction = st.slider("Satisfaction Score", 1.0, 5.0, 4.0)
    properties_owned = st.number_input("Properties Owned", 1, 20, 1)
    investment_value = st.number_input(
        "Total Investment Value ($)",
        50000,
        10000000,
        500000,
        step=50000,
    )
    average_property = st.number_input(
        "Average Property Value ($)",
        50000,
        5000000,
        500000,
        step=25000,
    )

with col2:
    floor_area = st.number_input(
        "Average Floor Area (sqft)",
        300,
        10000,
        1200,
        step=50,
    )
    client_type = st.selectbox("Client Type", ["Individual", "Corporate"])
    acquisition = st.selectbox(
        "Acquisition Purpose",
        ["Personal Use", "Investment"],
    )
    loan = st.selectbox("Loan Applied", ["Yes", "No"])

st.divider()

if st.button("Predict buyer segment"):
    client_type_corp = 1 if client_type == "Corporate" else 0
    investment_purpose = 1 if acquisition == "Investment" else 0
    loan_flag = 1 if loan == "Yes" else 0

    investment_intensity = investment_value / max(properties_owned, 1)
    portfolio_size_score = properties_owned * average_property
    investment_density = investment_value / max(floor_area, 1)
    engagement_score = satisfaction * properties_owned

    input_df = pd.DataFrame(
        [
            {
                "age": age,
                "satisfaction_score": satisfaction,
                "total_properties_owned": properties_owned,
                "total_investment_value": investment_value,
                "average_property_value": average_property,
                "average_floor_area": floor_area,
                "client_type_corp": client_type_corp,
                "investment_purpose": investment_purpose,
                "loan_flag": loan_flag,
                "investment_intensity": investment_intensity,
                "portfolio_size_score": portfolio_size_score,
                "investment_density": investment_density,
                "engagement_score": engagement_score,
            }
        ]
    )

    scaled = scaler.transform(input_df)
    cluster = int(kmeans.predict(scaled)[0])

    cluster_map = (
        buyer_profile[["cluster", "buyer_segment"]]
        .drop_duplicates()
        .set_index("cluster")["buyer_segment"]
        .to_dict()
    )

    predicted_segment = cluster_map.get(cluster, f"Cluster {cluster}")

    st.success(f"Predicted buyer segment: {predicted_segment}")

    st.subheader("Strategic recommendation")

    recommendations = {
        "First-Time Buyers": (
            "Recommend affordable residential properties, financing assistance, and first-home purchase incentives."
        ),
        "Corporate Investors": (
            "Recommend commercial portfolios, bulk purchase discounts, and dedicated relationship management."
        ),
        "Global Investors": (
            "Recommend premium investment properties, international investment services, and portfolio diversification options."
        ),
        "Luxury Investors": (
            "Recommend luxury developments, exclusive property previews, and concierge investment services."
        ),
        "Diversified Investors": (
            "Recommend mixed-use portfolios, diversification strategies, and personalized investment advisory services."
        ),
    }

    st.info(recommendations.get(predicted_segment, "General investment advisory recommended."))

    st.divider()

    st.subheader("Input summary")

    st.dataframe(input_df.T.rename(columns={0: "Value"}), use_container_width=True)