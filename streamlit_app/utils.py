import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    buyer_profile = pd.read_csv('../data/processed/buyer_segmented_dataset.csv')
    return buyer_profile