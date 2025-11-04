import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supplier Analytics Dashboard", layout="wide")
st.title("📊 Supplier Analytics Dashboard")
st.caption("Developed in Python + Streamlit (Colab Runtime)")

# --------------------
# Load Data
# --------------------
df = pd.read_csv("supply_chain_data.csv")  # uses your file
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# --------------------
# Numeric Columns
# --------------------
num_cols = ['price','availability','number_of_products_sold','revenue_generated',
            'stock_levels','lead_times','order_quantities','shipping_times','shipping_costs',
            'lead_time','production_volumes','manufacturing_lead_time','manufacturing_costs',
            'defect_rates','costs']

for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

st.sidebar.header("🔍 Filters")

# Detect possible supplier column automatically
possible_supplier_cols = [c for c in df.columns if "supplier" in c]
supplier_col = possible_supplier_cols[0] if possible_supplier_cols else None

if supplier_col:
    suppliers = sorted(df[supplier_col].dropna().unique())
    supplier_filter = st.sidebar.multiselect("Select Supplier(s)", suppliers)
    if supplier_filter:
        df = df[df[supplier_col].isin(supplier_filter)]
else:
    st.warning("⚠️ No supplier column found in data. Showing full dataset.")

# --------------------
# Supplier Summary
# --------------------
if supplier_col and {'revenue_generated','lead_time','production_volumes'}.issubset(df.columns):
    st.subheader("Supplier Performance Summary")
    supplier_summary = df.groupby(supplier_col).agg({
        'revenue_generated':'sum',
        'manufacturing_costs':'mean' if 'manufacturing_costs' in df.columns else 'mean',
        'defect_rates':'mean' if 'defect_rates' in df.columns else 'mean',
        'lead_time':'mean',
        'production_volumes':'sum',
        'shipping_costs':'mean' if 'shipping_costs' in df.columns else 'mean'
    }).reset_index()
    st.dataframe(supplier_summary)
else:
    st.info("ℹ️ Supplier summary not generated (missing supplier or key metric columns).")

# --------------------
# Route-wise Average Cost
# --------------------
if {'origin','destination','shipping_costs'}.issubset(df.columns):
    st.subheader("🚚 Route-wise Average Cost")
    route_summary = df.groupby(['origin','destination'])['shipping_costs'].mean().reset_index()
    st.dataframe(route_summary)

# --------------------
# Top 5 Most Demanded Products
# --------------------
if {'product_name','order_quantities'}.issubset(df.columns):
    st.subheader("🔥 Top 5 Most Demanded Products")
    top_demand = df.groupby('product_name')['order_quantities'].sum().reset_index().sort_values(
        'order_quantities', ascending=False).head(5)
    st.dataframe(top_demand)

# --------------------
# Origin-wise Supply
# --------------------
if {'origin','order_quantities','revenue_generated'}.issubset(df.columns):
    st.subheader("📦 Origin-wise Supply Summary")
    origin_summary = df.groupby('origin').agg({
        'order_quantities':'sum',
        'revenue_generated':'sum'
    }).reset_index()
    st.dataframe(origin_summary)

st.success("✅ Dashboard loaded successfully.")
