from pathlib import Path

import pandas as pd
import streamlit as st


# Project root: E:\Buyer_Segmentation_Real_Estate
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_data():
    """Load the final buyer segmentation dataset."""
    data_path = DATA_DIR / "buyer_segmented_dataset.csv"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Required dataset not found: {data_path}"
        )

    return pd.read_csv(data_path)


def metric_card(title, value):
    """Render a reusable executive KPI card."""
    st.markdown(
        f"""
        <div style="
            padding:18px;
            border-radius:14px;
            background:#F8FAFC;
            border:1px solid #E5E7EB;
            margin-bottom:10px;
        ">
            <div style="
                font-size:14px;
                color:#64748B;
                margin-bottom:5px;
            ">
                {title}
            </div>

            <div style="
                font-size:28px;
                font-weight:700;
                color:#0F172A;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )