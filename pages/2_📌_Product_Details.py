import streamlit as st
import pandas as pd
import os
from utils import segment_badge, product_card

st.set_page_config(page_title="Product Details", page_icon="📌", layout="wide")
st.title("📌 Product Details (Drill-down)")

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

# Product selector
product = st.selectbox("Select a product", sorted(df["product_name"].astype(str).unique().tolist()))
row = df[df["product_name"] == product].iloc[0]

# Product Card Display
st.markdown(product_card(row), unsafe_allow_html=True)

st.divider()

# Display
left, right = st.columns([2, 1])

with left:
    st.markdown("### 💰 Pricing")
    c1, c2, c3 = st.columns(3)
    c1.metric("Actual Price", f"₹{row['actual_price']:.0f}")
    c2.metric("Discounted Price", f"₹{row['discounted_price']:.0f}")
    c3.metric("Discount %", f"{row['discount_percentage']:.1f}%")

    st.markdown("### ⭐ Customer Feedback")
    c4, c5 = st.columns(2)
    c4.metric("Rating", f"{row['rating']:.2f}")
    c5.metric("Rating Count", f"{int(row['rating_count']):,}")

with right:
    st.markdown("### 🧠 Intelligence Scores")
    st.metric("Value Score", f"{row['value_score']:.1f}")
    st.metric("Trust Score", f"{row['trust_score']:.1f}")
    st.metric("Popularity Score", f"{row['popularity_score']:.1f}")

    st.markdown("### ✅ Recommendation")
    if row["value_score"] >= 80 and row["trust_score"] >= 70:
        st.success("🔥 Highly recommended deal (High value + High trust).")
    elif row["discount_percentage"] >= 60 and row["trust_score"] < 40:
        st.warning("⚠️ Discount Trap risk: High discount but low trust.")
    elif row["trust_score"] >= 80 and row["popularity_score"] < 25:
        st.info("💎 Hidden Gem: High trust but low visibility.")
    else:
        st.write("Balanced product — check reviews and price trend.")

st.divider()

# Reviews section (if columns exist)
st.subheader("📝 Review Snippets")
if "review_title" in df.columns or "review_content" in df.columns:
    st.write("Showing review text available in dataset for this product (if present).")

    if "review_title" in df.columns:
        st.markdown("**Review Title:**")
        st.write(row.get("review_title", "—"))

    if "review_content" in df.columns:
        st.markdown("**Review Content:**")
        st.write(row.get("review_content", "—"))
else:
    st.info("No review text columns found in dataset.")
