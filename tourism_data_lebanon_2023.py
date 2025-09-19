import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    url = "https://linked.aub.edu.lb/pkgcube/data/551015b5649368dd2612f795c2a9c2d8_20240902_115953.csv"
    return pd.read_csv(url)

df = load_data()

st.title("📊 Tourism Infrastructure & Initiatives Dashboard")
st.write("""
This dashboard explores tourism infrastructure (hotels, guest houses, cafes, restaurants) 
across towns, and how initiatives in the past five years impact the Tourism Index.
""")

st.sidebar.header("Filters")

towns = st.sidebar.multiselect(
    "Select Town(s):",
    options=df['Town'].unique(),
    default=df['Town'].unique()
)

initiative_filter = st.sidebar.radio(
    "Show towns with initiatives?",
    options=["All", "Yes", "No"]
)

filtered_df = df[df['Town'].isin(towns)]

if initiative_filter == "Yes":
    filtered_df = filtered_df[filtered_df['Existence of initiatives and projects in the past five years to improve the tourism sector - exists'] == 1]
elif initiative_filter == "No":
    filtered_df = filtered_df[filtered_df['Existence of initiatives and projects in the past five years to improve the tourism sector - exists'] == 0]

st.subheader("🌇 Tourism Infrastructure by Town")
fig1 = px.bar(
    filtered_df,
    x='Town',
    y=['Total number of hotels', 'Total number of restaurants', 'Total number of cafes', 'Total number of guest houses'],
    title="Towns split into 4 infrastructure categories",
    labels={'value':'Number of Facilities','variable':'Facility Type'},
    text_auto=True
)
fig1.update_layout(barmode='stack')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🥐Cafes vs 🍕Restaurants per Town")
fig2 = px.scatter(
    filtered_df,
    x='Total number of cafes',
    y='Total number of restaurants',
    size='Tourism Index',
    color='Existence of initiatives and projects in the past five years to improve the tourism sector - exists',
    hover_data=['Town'],
    title='In Relation to Tourism Index & Initiatives'
)
fig2.update_traces(textposition='top center')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("💡🕵️‍♀️ Context & Insights")
st.markdown("""
- The "Tourism Infrastructure by Town" chart covers the overall diversity of hotels, guest houses, restaurants, and cafes.
- The chart right below titled "Cafes vs Restaurants per Town" showcases the influence of the local initiatives in the last 5 years (like opening restaurants & cafes) to the tourism index per town.
- Towns with a high tourism index but limited tourism infrastructure could indicate great prospects for new business ventures under the hospitality industry (including restaurants & cafes).
- Towns with initiatives but low tourism index may indicate the need for town level marketing interventions to reach a wider audience and greater mass appeal.
""")
