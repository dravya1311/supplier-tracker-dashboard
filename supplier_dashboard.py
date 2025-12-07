# ===============================
# 📦 Supplier Tracker Dashboard
# Developed by Ravi Yadav | 2025
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------
# 🎨 Page Config
# ----------------------------------------
st.set_page_config(page_title="Supplier Tracker Dashboard", page_icon="📊", layout="wide")

# ----------------------------------------
# 🏷️ Title Section
# ----------------------------------------
st.markdown("""
    <h1 style='text-align:center; color:#2C3E50;'>📊 Supplier Tracker Dashboard</h1>
    <h5 style='text-align:center; color:#7F8C8D;'>End-to-End Supply Chain Insights | Developed by <b>Ravi Yadav</b></h5>
    <hr style='border:1px solid #BDC3C7;'>
""", unsafe_allow_html=True)

# ----------------------------------------
# 📁 Data Load
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_data.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

df = load_data()

# ----------------------------------------
# 🧮 Data Preparation
# ----------------------------------------
df['revenue_generated'] = pd.to_numeric(df['revenue_generated'], errors='coerce')
df['costs'] = pd.to_numeric(df['costs'], errors='coerce')
df['production_volumes'] = pd.to_numeric(df['production_volumes'], errors='coerce')
df['lead_time'] = pd.to_numeric(df['lead_time'], errors='coerce')
df['number_of_products_sold'] = pd.to_numeric(df['number_of_products_sold'], errors='coerce')

# ----------------------------------------
# 🎛️ Sidebar Filters
# ----------------------------------------
st.sidebar.header("🔍 Filters")
supplier_filter = st.sidebar.multiselect("Select Supplier(s)", df['supplier_name'].unique())
origin_filter = st.sidebar.multiselect("Select Origin(s)", df['origin'].unique())
destination_filter = st.sidebar.multiselect("Select Destination(s)", df['destination'].unique())

filtered_df = df.copy()
if supplier_filter:
    filtered_df = filtered_df[filtered_df['supplier_name'].isin(supplier_filter)]
if origin_filter:
    filtered_df = filtered_df[filtered_df['origin'].isin(origin_filter)]
if destination_filter:
    filtered_df = filtered_df[filtered_df['destination'].isin(destination_filter)]

# ----------------------------------------
# 🔢 KPI Summary Cards
# ----------------------------------------
total_revenue = filtered_df['revenue_generated'].sum()
total_cost = filtered_df['costs'].sum()
total_volume = filtered_df['production_volumes'].sum()
avg_lead_time = filtered_df['lead_time'].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
kpi2.metric("💸 Total Cost", f"₹{total_cost:,.0f}")
kpi3.metric("🏭 Total Production Volume", f"{total_volume:,.0f}")
kpi4.metric("⏱️ Avg Lead Time (Days)", f"{avg_lead_time:.1f}")

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------
# 📈 Tabs Section
# ----------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛣️ Route Cost", "🏭 Supplier Performance", "📦 Product Demand",
    "🌍 Origin Overview", "💹 Cost vs Revenue Trend"
])

# --- Route Cost ---
with tab1:
    st.subheader("🛣️ Average Route-wise Cost")
    route_df = filtered_df.groupby(['origin', 'destination'])['costs'].mean().reset_index()
    fig1 = px.density_heatmap(route_df, x='origin', y='destination', z='costs',
                              color_continuous_scale='Blues', title="Average Route Cost Heatmap",
                              template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

# --- Supplier Performance ---
with tab2:
    st.subheader("🏭 Top Suppliers by Production Volume")
    supplier_vol = filtered_df.groupby(['supplier_name', 'product_type'])['production_volumes'].sum().reset_index()
    top_suppliers = supplier_vol.groupby('supplier_name')['production_volumes'].sum().nlargest(5).index
    top_df = supplier_vol[supplier_vol['supplier_name'].isin(top_suppliers)]
    fig2 = px.bar(top_df, x='supplier_name', y='production_volumes', color='product_type',
                  text_auto=False, title="Top 5 Suppliers by Product Type",
                  template='plotly_white', color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig2, use_container_width=True)

# --- Product Demand ---
with tab3:
    st.subheader("📦 Top 5 Most Demanded Products")
    demand_df = filtered_df.groupby('product_type')['number_of_products_sold'].sum().nlargest(5).reset_index()
    fig3 = px.bar(demand_df, x='product_type', y='number_of_products_sold',
                  color='product_type', text_auto=True,
                  title="Top 5 Most Demanded Products", template='plotly_white',
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig3, use_container_width=True)

# --- Origin Overview ---
with tab4:
    st.subheader("🌍 Origin-wise Supply & Revenue")
    origin_df = filtered_df.groupby('origin')[['production_volumes', 'revenue_generated']].sum().reset_index()
    fig4 = px.treemap(origin_df, path=['origin'], values='production_volumes',
                      color='revenue_generated', color_continuous_scale='viridis',
                      title="Origin-wise Supply (Size) & Revenue (Color)")
    st.plotly_chart(fig4, use_container_width=True)

# --- Cost vs Revenue Trend ---
with tab5:
    st.subheader("💹 Cost vs Revenue by Supplier")
    trend_df = filtered_df.groupby('supplier_name')[['revenue_generated', 'costs']].sum().reset_index()
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=trend_df['supplier_name'], y=trend_df['revenue_generated'],
                          name='Revenue', marker_color='green'))
    fig5.add_trace(go.Bar(x=trend_df['supplier_name'], y=trend_df['costs'],
                          name='Cost', marker_color='red'))
    fig5.update_layout(barmode='group', template='plotly_white',
                       title="Cost vs Revenue by Supplier", xaxis_title="Supplier",
                       yaxis_title="Value (₹)")
    st.plotly_chart(fig5, use_container_width=True)

# ----------------------------------------
# 📄 Footer
# ----------------------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:grey;'>
Developed by <b>Ravi Yadav</b> | Supply Chain Analytics | © 2025
</p>
""", unsafe_allow_html=True)



