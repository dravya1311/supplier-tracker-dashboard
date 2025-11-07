import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    layout="wide",
    page_icon="📦"
)

# ---- HEADER ----
st.title("📊 Supply Chain Analytics Dashboard")
st.caption("Developed by **Ravi Yadav** | Powered by Python + Streamlit")

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# ---- SIDEBAR FILTERS ----
st.sidebar.header("🔍 Filters")

origins = df['origin'].dropna().unique().tolist()
destinations = df['destination'].dropna().unique().tolist()
suppliers = df['supplier name'].dropna().unique().tolist()

origin_filter = st.sidebar.multiselect("Select Origin(s):", origins)
destination_filter = st.sidebar.multiselect("Select Destination(s):", destinations)
supplier_filter = st.sidebar.multiselect("Select Supplier(s):", suppliers)

filtered_df = df.copy()
if origin_filter:
    filtered_df = filtered_df[filtered_df['origin'].isin(origin_filter)]
if destination_filter:
    filtered_df = filtered_df[filtered_df['destination'].isin(destination_filter)]
if supplier_filter:
    filtered_df = filtered_df[filtered_df['supplier name'].isin(supplier_filter)]

# ---- DASHBOARD CONTENT ----
st.markdown("### 🚚 Logistics Overview")

if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total Products", len(filtered_df))
    col2.metric("💰 Total Revenue", f"${filtered_df['revenue generated'].sum():,.2f}")
    col3.metric("📦 Avg. Lead Time", f"{filtered_df['lead time'].mean():.1f} days")

    st.divider()

    # ---- CHARTS ----
    st.markdown("### 🌎 Route-wise Cost Analysis")
    if 'routes' in filtered_df.columns and 'costs' in filtered_df.columns:
        route_chart = px.bar(
            filtered_df,
            x='routes',
            y='costs',
            color='origin',
            title="Transportation Costs by Route",
            template="plotly_dark"
        )
        st.plotly_chart(route_chart, use_container_width=True)

    st.markdown("### 🏭 Supplier Performance Overview")
    if 'supplier name' in filtered_df.columns and 'production volumes' in filtered_df.columns:
        supplier_chart = px.bar(
            filtered_df,
            x='supplier name',
            y='production volumes',
            color='supplier name',
            title="Supplier Production Volume",
            template="plotly_dark"
        )
        st.plotly_chart(supplier_chart, use_container_width=True)

    st.markdown("### 📈 Revenue by Product Type")
    if 'product type' in filtered_df.columns and 'revenue generated' in filtered_df.columns:
        revenue_chart = px.pie(
            filtered_df,
            names='product type',
            values='revenue generated',
            title="Revenue Distribution by Product Type",
            hole=0.4
        )
        st.plotly_chart(revenue_chart, use_container_width=True)

    st.markdown("### 🕒 Lead Time Distribution")
    if 'lead time' in filtered_df.columns:
        lead_chart = px.histogram(
            filtered_df,
            x='lead time',
            nbins=20,
            title="Distribution of Lead Times",
            template="simple_white"
        )
        st.plotly_chart(lead_chart, use_container_width=True)
else:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")

# ---- FOOTER ----
st.divider()
st.markdown(
    "<p style='text-align:center;'>📊 Supply Chain Dashboard | Designed by <b>Ravi Yadav</b></p>",
    unsafe_allow_html=True
)
