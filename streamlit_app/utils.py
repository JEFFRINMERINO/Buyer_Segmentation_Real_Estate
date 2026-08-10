import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """Load the buyer segmented dataset."""
    return pd.read_csv('../data/processed/buyer_segmented_dataset.csv')

def metric_card(title, value):
    """Display a styled KPI card."""
    st.markdown(
        f"""
        <div style='
            padding:18px;
            border-radius:14px;
            background:#F8FAFC;
            border:1px solid #E5E7EB;
            box-shadow:0 1px 3px rgba(0,0,0,0.05);
            margin-bottom:10px;
        '>
            <div style='font-size:14px;color:#64748B;font-weight:500;'>{title}</div>
            <div style='font-size:28px;font-weight:700;color:#0F172A;margin-top:6px;'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )