import streamlit as st
import plotly.express as px
from utils import load_data, metric_card

st.set_page_config(
    page_title='Real Estate Market Intelligence',
    page_icon='🏢',
    layout='wide'
)

buyer_profile = load_data()

total_buyers = buyer_profile["client_id"].nunique()

total_investment = buyer_profile["total_investment_value"].sum()

average_age = buyer_profile["age"].mean()

average_satisfaction = buyer_profile["satisfaction_score"].mean()

st.title('🏢 Real Estate Market Intelligence Dashboard')
st.markdown('### AI-powered buyer segmentation and investment profiling')

st.markdown(
    """
    <div style="padding:20px;border-radius:16px;background:#EFF6FF;border:1px solid #DBEAFE;margin-bottom:20px;">
        <h3 style="color:#1D4ED8;margin-bottom:8px;">AI-powered real estate market intelligence</h3>
        <p style="color:#334155;margin:0;">
        Identify high-value buyer segments, investment behavior patterns, financing preferences,
        and geographic opportunities using machine learning clustering and interactive analytics.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    st.metric(
        label="Total Buyers",
        value=f"{total_buyers:,}"
    )

with col2:
    st.metric(
        label="Total Investment Value",
        value=f"${total_investment:,.0f}"
    )

with col3:
    st.metric(
        label="Average Age",
        value=f"{average_age:.1f}"
    )

with col4:
    st.metric(
        label="Average Satisfaction",
        value=f"{average_satisfaction:.2f}"
    )

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

top_segment = filtered['buyer_segment'].value_counts().idxmax()

st.markdown(
    f"""
    ### Executive insight

    The **{top_segment}** segment currently represents the largest buyer population in the filtered dataset.

    This segment should be prioritized for targeted marketing campaigns, personalized property recommendations,
    and investment-focused customer engagement strategies.
    """
)

st.dataframe(summary, use_container_width=True)

st.markdown("---")

csv = filtered.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download filtered buyer data",
    data=csv,
    file_name="buyer_segmented_data.csv",
    mime="text/csv"
)

st.caption("Built with Streamlit, Plotly, and Scikit-learn")