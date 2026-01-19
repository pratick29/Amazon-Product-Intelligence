import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Review Intelligence", page_icon="🧾", layout="wide")
st.title("🧾 Review Intelligence (NLP)")
st.caption("Sentiment + risky keyword detection from customer reviews")

@st.cache_data
def load_data():
    file_path = "outputs/scored_segmented_products.csv"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return None
    return pd.read_csv(file_path)

df = load_data()
if df is None:
    st.error("❌ Data not found.")
    st.stop()

if "sentiment_score" not in df.columns or "risk_flag" not in df.columns:
    st.error("❌ NLP columns not found. Please run notebook NLP step and export again.")
    st.stop()

df["main_category"] = df["category"].astype(str).apply(lambda x: x.split("|")[0])

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Avg Sentiment Score", f"{df['sentiment_score'].mean():.2f}")
c2.metric("Risk Flag Count", f"{int(df['risk_flag'].sum()):,}")
c3.metric("Risk %", f"{(df['risk_flag'].mean()*100):.2f}%")

st.divider()

# Sentiment distribution
st.subheader("📊 Sentiment Distribution")
fig = plt.figure()
plt.hist(df["sentiment_score"].dropna(), bins=20)
plt.xlabel("Sentiment (VADER compound)")
plt.ylabel("Count")
st.pyplot(fig)

st.divider()

# Risky products table
st.subheader("🚨 High Risk Products (keyword flagged)")
risky = df[df["risk_flag"] == 1].copy()

cols = [
    "product_name", "main_category", "segment_name",
    "discounted_price", "discount_percentage",
    "rating", "rating_count",
    "sentiment_score", "risk_flag",
    "review_title"
]
cols = [c for c in cols if c in risky.columns]

st.dataframe(
    risky.sort_values(["sentiment_score", "trust_score"], ascending=True)[cols].head(50),
    use_container_width=True,
    height=520
)
