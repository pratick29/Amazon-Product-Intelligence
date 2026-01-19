import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Insights & Explainability", page_icon="🧠", layout="wide")
st.title("🧠 Insights & Explainability")

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

# ---------------- Auto Insights ----------------
st.subheader("📌 Auto-Generated Insights")

insights = []

# insight: highest avg discount category
tmp = df.groupby("main_category")["discount_percentage"].mean().sort_values(ascending=False)
if len(tmp):
    insights.append(f"🔻 Highest average discount category: **{tmp.index[0]}** ({tmp.iloc[0]:.1f}%).")

# insight: most trusted category
tmp = df.groupby("main_category")["trust_score"].mean().sort_values(ascending=False)
if len(tmp):
    insights.append(f"✅ Most trusted category: **{tmp.index[0]}** (Avg trust {tmp.iloc[0]:.1f}).")

# insight: discount traps size
if "segment_name" in df.columns:
    trap_count = (df["segment_name"] == "Discount Trap").sum()
    insights.append(f"⚠️ Products flagged as Discount Trap: **{trap_count:,}**.")

# insight: best deals size
if "segment_name" in df.columns:
    best_count = (df["segment_name"] == "Best Deals").sum()
    insights.append(f"🔥 Products in Best Deals segment: **{best_count:,}**.")

for i in insights:
    st.write(i)

st.divider()

# ---------------- Explainability ----------------
st.subheader("🔎 Explainability: How Scores Work")

with st.expander("📌 Value Score explanation"):
    st.markdown("""
**Value Score** measures deal attractiveness.  
It combines:
- Discount component (higher discount → higher value)
- Price component (lower discounted price → higher value)

> Example: High discount + affordable price = high Value Score
""")

with st.expander("📌 Trust Score explanation"):
    st.markdown("""
**Trust Score** is based on a weighted rating logic.

Why weighted?
- A product with rating 5.0 but only 2 reviews isn't reliable.
- A product with rating 4.2 and 5000 reviews is more trustworthy.

So Trust Score uses:
✅ rating  
✅ rating_count  
to create a more stable quality signal.
""")

with st.expander("📌 Popularity Score explanation"):
    st.markdown("""
**Popularity Score** is computed from normalized `rating_count`.  
Higher rating_count generally means:
- higher visibility
- higher sales likelihood
- more buyer engagement
""")

st.info("This transparency improves dashboard credibility and makes the project more interview-ready.")
