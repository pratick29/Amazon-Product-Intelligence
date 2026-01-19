import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Product Explorer", page_icon="🔍", layout="wide")
st.title("🔍 Product Explorer")
st.caption("Search, filter, and explore Amazon products with Value/Trust scoring + segments + NLP risk alerts.")

# ---------- Load data ----------
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

# ---------- Derived fields ----------
df["main_category"] = df["category"].astype(str).apply(lambda x: x.split("|")[0])

# ---------- UI Helpers ----------
def segment_badge(segment):
    colors = {
        "Best Deals": "#16a34a",
        "Discount Trap": "#dc2626",
        "Hidden Gems": "#2563eb",
        "Premium Picks": "#d97706",
        "Market Leaders": "#7c3aed",
    }
    bg = colors.get(segment, "#6b7280")

    return f"""
    <span style="
        background:{bg};
        color:white;
        padding:5px 10px;
        border-radius:999px;
        font-size:12px;
        font-weight:700;">
        {segment}
    </span>
    """

def sentiment_emoji(score):
    if pd.isna(score):
        return "—"
    if score >= 0.35:
        return "😄 Positive"
    if score <= -0.20:
        return "😡 Negative"
    return "😐 Neutral"

def get_badge(row):
    # priority-based deal badges
    if row["value_score"] >= 80 and row["trust_score"] >= 70:
        return "🔥 Hot Deal"
    if row["discount_percentage"] >= 60 and row["trust_score"] < 40:
        return "⚠️ Discount Trap"
    if row["trust_score"] >= 80 and row["popularity_score"] < 25:
        return "💎 Hidden Gem"
    if row["trust_score"] >= 85:
        return "🏆 Top Rated"
    if row["discount_percentage"] >= 50:
        return "✅ Best Value"
    return "—"

df["deal_badge"] = df.apply(get_badge, axis=1)

def product_card(row):
    seg = row.get("segment_name", "—")
    sentiment = row.get("sentiment_score", np.nan)
    risk = row.get("risk_flag", 0)

    risk_text = "🚨 Risky keywords found in reviews" if risk == 1 else "✅ No risky keywords detected"
    sentiment_text = sentiment_emoji(sentiment)

    return f"""
    <div style="
        border:1px solid #e5e7eb;
        border-radius:18px;
        padding:16px;
        margin-bottom:14px;
        background:white;
        box-shadow:0 2px 10px rgba(0,0,0,0.06);">

        <div style="display:flex;justify-content:space-between;gap:10px;">
            <div style="font-size:16px;font-weight:800;line-height:1.3;">
                {row['product_name']}
            </div>
            <div style="font-size:13px;font-weight:700;color:#111827;">
                {row.get('deal_badge','—')}
            </div>
        </div>

        <div style="color:#6b7280;margin-top:6px;font-size:13px;">
            {row.get('main_category','—')}
        </div>

        <div style="display:flex; gap:14px; flex-wrap:wrap; margin-top:10px; font-size:14px;">
            <div>💰 <b>₹{row['discounted_price']:.0f}</b></div>
            <div>🔻 <b>{row['discount_percentage']:.1f}%</b></div>
            <div>⭐ <b>{row['rating']:.2f}</b> ({int(row['rating_count']):,})</div>
        </div>

        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px; font-size:13px;">
            <div>🎯 Value: <b>{row['value_score']:.1f}</b></div>
            <div>🛡 Trust: <b>{row['trust_score']:.1f}</b></div>
            <div>📈 Popularity: <b>{row['popularity_score']:.1f}</b></div>
        </div>

        <div style="margin-top:12px; display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;">
            <div>{segment_badge(seg)}</div>
            <div style="color:#374151; font-weight:600;">{sentiment_text}</div>
            <div style="color:{'#dc2626' if risk==1 else '#16a34a'}; font-weight:700;">
                {risk_text}
            </div>
        </div>
    </div>
    """

# ---------- Sidebar Filters ----------
st.sidebar.header("🔎 Filters")

search_query = st.sidebar.text_input("Search product name", "")

category_list = ["All"] + sorted(df["main_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", category_list)

segment_list = ["All"] + sorted(df["segment_name"].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("Segment", segment_list)

min_price, max_price = float(df["discounted_price"].min()), float(df["discounted_price"].max())
price_range = st.sidebar.slider("Discounted Price Range", min_price, max_price, (min_price, max_price))

min_discount, max_discount = float(df["discount_percentage"].min()), float(df["discount_percentage"].max())
discount_range = st.sidebar.slider("Discount % Range", min_discount, max_discount, (min_discount, max_discount))

min_rating, max_rating = float(df["rating"].min()), float(df["rating"].max())
rating_range = st.sidebar.slider("Rating Range", min_rating, max_rating, (min_rating, max_rating))

show_only_risky = st.sidebar.checkbox("Show only risky products 🚨", value=False)

max_cards = st.sidebar.slider("Cards to render (performance)", 0, 30, 10)

limit = st.sidebar.slider("Rows to display (table)", 50, 5000, 500)

# ---------- Apply Filters ----------
filtered = df.copy()

if search_query.strip():
    filtered = filtered[filtered["product_name"].astype(str).str.contains(search_query, case=False, na=False)]

if selected_category != "All":
    filtered = filtered[filtered["main_category"] == selected_category]

if selected_segment != "All":
    filtered = filtered[filtered["segment_name"] == selected_segment]

filtered = filtered[
    (filtered["discounted_price"] >= price_range[0]) &
    (filtered["discounted_price"] <= price_range[1]) &
    (filtered["discount_percentage"] >= discount_range[0]) &
    (filtered["discount_percentage"] <= discount_range[1]) &
    (filtered["rating"] >= rating_range[0]) &
    (filtered["rating"] <= rating_range[1])
]

if show_only_risky and "risk_flag" in filtered.columns:
    filtered = filtered[filtered["risk_flag"] == 1]

# ---------- KPI Bar ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Products", f"{len(filtered):,}")
k2.metric("Avg Rating", f"{filtered['rating'].mean():.2f}" if len(filtered) else "—")
k3.metric("Avg Discount %", f"{filtered['discount_percentage'].mean():.2f}%" if len(filtered) else "—")
k4.metric("Avg Trust Score", f"{filtered['trust_score'].mean():.2f}" if len(filtered) else "—")

st.divider()

# ---------- Cards view ----------
st.subheader("✨ Top Products (Cards View)")
top_cards = filtered.sort_values(["trust_score", "value_score"], ascending=False).head(max_cards)

if max_cards == 0:
    st.info("Cards disabled for performance. Enable from sidebar.")
elif len(top_cards) == 0:
    st.warning("No products found for your filters.")
else:
    for _, r in top_cards.iterrows():
        st.markdown(product_card(r), unsafe_allow_html=True)

st.divider()

# ---------- Table view ----------
st.subheader("📋 Full Results (Table View)")

display_cols = [
    "deal_badge",
    "product_name",
    "main_category",
    "segment_name",
    "discounted_price",
    "discount_percentage",
    "rating",
    "rating_count",
    "value_score",
    "trust_score",
    "popularity_score",
    "sentiment_score",
    "risk_flag",
]
display_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered[display_cols].sort_values(["trust_score", "value_score"], ascending=False),
    use_container_width=True,
    height=520
)

st.download_button(
    "⬇️ Download Filtered Data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_products.csv",
    mime="text/csv"
)
