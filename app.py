import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Amazon Product Intelligence Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Amazon Product Intelligence Dashboard")
st.caption("EDA + Value/Trust/Popularity Scoring + Segmentation + Decision Intelligence")

st.markdown("""
### ✅ What this dashboard helps with
- Identify **Best Deals** (high value + high trust)
- Detect **Discount Traps** (high discount + low trust)
- Discover **Hidden Gems** (high trust but low popularity)
- Compare **category-level pricing + quality signals**
- Provide decision-ready product recommendations
""")

st.info("Use the left sidebar to navigate pages: Product Explorer, Product Details, Category Intelligence, Insights.")

# Quick data check
file_path = "outputs/scored_segmented_products.csv"
if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
    st.error("❌ outputs/scored_segmented_products.csv is missing or empty. Run the notebook and export it.")
    st.stop()

df = pd.read_csv(file_path)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", f"{len(df):,}")
col2.metric("Avg Rating", f"{df['rating'].mean():.2f}")
col3.metric("Avg Discount %", f"{df['discount_percentage'].mean():.2f}%")
col4.metric("Avg Trust Score", f"{df['trust_score'].mean():.2f}")
