import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Category Intelligence", page_icon="📊", layout="wide")
st.title("📊 Category Intelligence")

@st.cache_data
def load_data():
    file_path = "outputs/scored_segmented_products.csv"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return None
    return pd.read_csv(file_path)

df = load_data()
if df is None:
    st.error("❌ Data not found. Export outputs/scored_segmented_products.csv from notebook.")
    st.stop()

df["main_category"] = df["category"].astype(str).apply(lambda x: x.split("|")[0])

st.markdown("""
This page provides **category-level marketplace insights**, useful for:
- promotion strategy
- quality monitoring
- discount policy optimization
""")

# Category KPIs
cat_summary = df.groupby("main_category").agg(
    product_count=("product_id", "count"),
    avg_discount=("discount_percentage", "mean"),
    avg_rating=("rating", "mean"),
    avg_value=("value_score", "mean"),
    avg_trust=("trust_score", "mean"),
    avg_popularity=("popularity_score", "mean"),
).reset_index().sort_values("product_count", ascending=False)

st.subheader("📌 Category Performance Table")
st.dataframe(cat_summary, use_container_width=True, height=520)

st.divider()

# Chart
st.subheader("📈 Top Categories by Product Count")
topn = st.slider("Top N categories", 5, 30, 10)

top = cat_summary.head(topn)

fig = plt.figure()
plt.bar(top["main_category"], top["product_count"])
plt.xticks(rotation=40, ha="right")
plt.xlabel("Category")
plt.ylabel("Product Count")
st.pyplot(fig)
