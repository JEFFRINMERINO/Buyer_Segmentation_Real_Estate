import streamlit as st
import plotly.express as px
from utils import load_data, metric_card

st.set_page_config(
    page_title='Real Estate Market Intelligence',
    page_icon='🏢',
    layout='wide'
)

buyer_profile = load_data()

st.title('🏢 Real Estate Market Intelligence Dashboard')
st.markdown('### AI-powered buyer segmentation and investment profiling')

st.sidebar.header('Filters')

countries = ['All'] + sorted(buyer_profile['country'].dropna().unique().tolist())
regions = ['All'] + sorted(buyer_profile['region'].dropna().unique().tolist())

selected_country = st.sidebar.selectbox('Country', countries)
selected_region = st.sidebar.selectbox('Region', regions)

filtered = buyer_profile.copy()

if selected_country != 'All':
    filtered = filtered[filtered['country'] == selected_country]

if selected_region != 'All':
    filtered = filtered[filtered['region'] == selected_region]

total_buyers = len(filtered)
total_investment = filtered['total_investment_value'].sum()
avg_age = filtered['age'].mean()
avg_satisfaction = filtered['satisfaction_score'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Total Buyers", f"{total_buyers:,}")

with col2:
    metric_card("Total Investment Value", f"${total_investment:,.0f}")

with col3:
    metric_card("Average Age", f"{avg_age:.1f}")

with col4:
    metric_card("Average Satisfaction", f"{avg_satisfaction:.2f}")

st.divider()

st.subheader('Buyer Segment Distribution')

segment_counts = (
    filtered['buyer_segment']
    .value_counts()
    .reset_index()
)

segment_counts.columns = ['Buyer Segment', 'Buyers']

fig = px.bar(
    segment_counts,
    x='Buyer Segment',
    y='Buyers',
    color='Buyer Segment',
    text='Buyers'
)

fig.update_layout(
    template='plotly_white',
    height=450,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('Executive Summary')

summary = filtered.groupby('buyer_segment').agg(
    Buyers=('client_id', 'count'),
    Average_Investment=('total_investment_value', 'mean'),
    Average_Properties=('total_properties_owned', 'mean'),
    Average_Satisfaction=('satisfaction_score', 'mean')
).round(2)

st.dataframe(summary, use_container_width=True)

st.markdown('---')
st.caption('Built with Streamlit, Plotly, and Scikit-learn')