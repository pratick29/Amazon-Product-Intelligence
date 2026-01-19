import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Recommendation Engine", page_icon="🤝", layout="wide")
st.title("🤝 Recommendation Engine")
st.caption("Personalized product recommendations based on budget, category, rating, and trust/value preferences.")

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

# ---------------------
# User Inputs
# ---------------------
st.sidebar.header("🎛 Recommendation Settings")

category_list = ["All"] + sorted(df["main_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", category_list)

max_budget = st.sidebar.number_input(
    "Max Budget (₹)", 
    min_value=0, 
    max_value=int(df["discounted_price"].max()),
    value=min(2000, int(df["discounted_price"].max()))
)

min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.5, 0.1)

preference = st.sidebar.radio(
    "Preference",
    ["Best overall", "Best value (discount)", "Most trusted", "Most popular"]
)

top_n = st.sidebar.slider("How many recommendations?", 5, 50, 15)

# ---------------------
# Filtering
# ---------------------
data = df.copy()

if selected_category != "All":
    data = data[data["main_category"] == selected_category]

data = data[
    (data["discounted_price"] <= max_budget) &
    (data["rating"] >= min_rating)
].copy()

if len(data) == 0:
    st.warning("No products match your filters. Increase budget or lower minimum rating.")
    st.stop()

# ---------------------
# Ranking logic (RULE-BASED RECOMMENDER)
# ---------------------
# Normalize to combine fairly
def normalize(series):
    if series.max() == series.min():
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())

data["value_n"] = normalize(data["value_score"])
data["trust_n"] = normalize(data["trust_score"])
data["popularity_n"] = normalize(data["popularity_score"])

if preference == "Best overall":
    # strongest recommender formula
    data["final_score"] = 0.45 * data["trust_n"] + 0.35 * data["value_n"] + 0.20 * data["popularity_n"]
elif preference == "Best value (discount)":
    data["final_score"] = 0.60 * data["value_n"] + 0.25 * data["trust_n"] + 0.15 * data["popularity_n"]
elif preference == "Most trusted":
    data["final_score"] = 0.70 * data["trust_n"] + 0.20 * data["value_n"] + 0.10 * data["popularity_n"]
else:  # Most popular
    data["final_score"] = 0.70 * data["popularity_n"] + 0.20 * data["trust_n"] + 0.10 * data["value_n"]

recommendations = data.sort_values("final_score", ascending=False).head(top_n)

# ---------------------
# Display
# ---------------------
st.subheader("✅ Recommended Products")

cols = [
    "product_name", "main_category",
    "discounted_price", "discount_percentage",
    "rating", "rating_count",
    "value_score", "trust_score", "popularity_score",
    "segment_name"
]
cols = [c for c in cols if c in recommendations.columns]

st.dataframe(recommendations[cols], use_container_width=True, height=520)

st.download_button(
    "⬇️ Download Recommendations CSV",
    data=recommendations.to_csv(index=False).encode("utf-8"),
    file_name="recommended_products.csv",
    mime="text/csv"
)
