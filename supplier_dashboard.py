import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supplier Tracker Dashboard", page_icon="📦", layout="wide")

st.title("📊 Supplier Tracker Dashboard")
st.caption("Supply Chain Analytics — Origin Cost | Supplier | Product Demand")

uploaded_file = st.file_uploader("📂 Upload your supply_chain_data.csv", type=["csv"])

if uploaded_file:
    # Read and clean
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    st.success("✅ File uploaded successfully!")

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")
    suppliers = st.sidebar.multiselect("Select Supplier(s)", df['supplier_name'].unique())
    origins = st.sidebar.multiselect("Select Origin(s)", df['origin'].unique())
    destinations = st.sidebar.multiselect("Select Destination(s)", df['destination'].unique())

    filtered_df = df.copy()
    if suppliers:
        filtered_df = filtered_df[filtered_df['supplier_name'].isin(suppliers)]
    if origins:
        filtered_df = filtered_df[filtered_df['origin'].isin(origins)]
    if destinations:
        filtered_df = filtered_df[filtered_df['destination'].isin(destinations)]

    # KPIs
    total_revenue = filtered_df['revenue_generated'].sum()
    total_cost = filtered_df['costs'].sum()
    total_volume = filtered_df['production_volumes'].sum()
    avg_lead_time = filtered_df['lead_time'].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
    k2.metric("💸 Total Cost", f"₹{total_cost:,.0f}")
    k3.metric("🏭 Total Production Volume", f"{total_volume:,.0f}")
    k4.metric("⏱ Avg Lead Time (Days)", f"{avg_lead_time:.1f}")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛣️ Route Cost", "🏭 Supplier Performance", "📦 Product Demand", "🌍 Origin Overview"
    ])

    # --- Route Cost ---
    with tab1:
        route_df = filtered_df.groupby(['origin', 'destination'])['costs'].mean().reset_index()
        fig1 = px.scatter(route_df, x='origin', y='destination', size='costs', color='costs',
                          title="Average Route-wise Cost", color_continuous_scale='tealrose')
        st.plotly_chart(fig1, use_container_width=True)

    # --- Supplier Performance ---
    with tab2:
        supplier_vol = (filtered_df.groupby(['supplier_name', 'product_type'])
                        ['production_volumes'].sum().reset_index())
        top5_suppliers = supplier_vol.groupby('supplier_name')['production_volumes'].sum().nlargest(5).index
        top_df = supplier_vol[supplier_vol['supplier_name'].isin(top5_suppliers)]

        fig2 = px.bar(top_df, x='supplier_name', y='production_volumes',
                      color='product_type', text_auto=True,
                      title="Top 5 Suppliers by Production Volume (Product Split)",
                      template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)

    # --- Product Demand ---
    with tab3:
        demand_df = (filtered_df.groupby('product_type')['number_of_products_sold']
                     .sum().nlargest(5).reset_index())
        fig3 = px.bar(demand_df, x='product_type', y='number_of_products_sold',
                      color='product_type', text_auto=True,
                      title="Top 5 Most Demanded Products", template='seaborn')
        st.plotly_chart(fig3, use_container_width=True)

    # --- Origin Overview ---
    with tab4:
        origin_df = (filtered_df.groupby('origin')
                     .agg({'production_volumes': 'sum', 'revenue_generated': 'sum'})
                     .reset_index())
        fig4 = px.treemap(origin_df, path=['origin'], values='production_volumes',
                          color='revenue_generated', color_continuous_scale='viridis',
                          title="Origin-wise Supply & Revenue")
        st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("👆 Please upload your CSV file to view the dashboard.")
