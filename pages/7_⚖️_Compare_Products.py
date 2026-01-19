import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Compare Products", page_icon="⚖️", layout="wide")
st.title("⚖️ Compare Two Products")
st.caption("Side-by-side comparison using pricing, discount, ratings and your intelligence scores.")

@st.cache_data
def load_data():
    fp = "outputs/scored_segmented_products.csv"
    if not os.path.exists(fp) or os.path.getsize(fp) == 0:
        return None
    return pd.read_csv(fp)

df = load_data()
if df is None:
    st.error("❌ Data not found.")
    st.stop()

df["main_category"] = df["category"].astype(str).apply(lambda x: x.split("|")[0])

# Select products
products = sorted(df["product_name"].astype(str).unique().tolist())

colA, colB = st.columns(2)
with colA:
    p1 = st.selectbox("Choose Product A", products, index=0)
with colB:
    p2 = st.selectbox("Choose Product B", products, index=min(1, len(products)-1))

row1 = df[df["product_name"] == p1].iloc[0]
row2 = df[df["product_name"] == p2].iloc[0]

def metric_block(title, row):
    st.subheader(title)
    st.write(f"**Category:** {row['main_category']}")
    st.write(f"**Segment:** {row.get('segment_name', '—')}")
    st.write("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("Actual Price", f"₹{row['actual_price']:.0f}")
    c2.metric("Discounted Price", f"₹{row['discounted_price']:.0f}")
    c3.metric("Discount %", f"{row['discount_percentage']:.1f}%")

    c4, c5 = st.columns(2)
    c4.metric("Rating", f"{row['rating']:.2f}")
    c5.metric("Rating Count", f"{int(row['rating_count']):,}")

    st.write("---")
    c6, c7, c8 = st.columns(3)
    c6.metric("Value Score", f"{row['value_score']:.1f}")
    c7.metric("Trust Score", f"{row['trust_score']:.1f}")
    c8.metric("Popularity Score", f"{row['popularity_score']:.1f}")

    if "sentiment_score" in df.columns:
        st.metric("Sentiment", f"{row.get('sentiment_score', 0):.2f}")

    if "risk_flag" in df.columns:
        risk = int(row.get("risk_flag", 0))
        st.metric("Risk Flag", "🚨 Yes" if risk == 1 else "✅ No")

left, right = st.columns(2)
with left:
    metric_block("🅰️ Product A", row1)
with right:
    metric_block("🅱️ Product B", row2)

# Quick winner logic
st.divider()
st.subheader("🏆 Winner Suggestion")

scoreA = 0.45*row1["trust_score"] + 0.35*row1["value_score"] + 0.20*row1["popularity_score"]
scoreB = 0.45*row2["trust_score"] + 0.35*row2["value_score"] + 0.20*row2["popularity_score"]

if scoreA > scoreB:
    st.success(f"✅ Recommended: **{p1}** (higher overall intelligence score)")
elif scoreB > scoreA:
    st.success(f"✅ Recommended: **{p2}** (higher overall intelligence score)")
else:
    st.info("Both products score similarly. Prefer the one with higher Trust Score.")
