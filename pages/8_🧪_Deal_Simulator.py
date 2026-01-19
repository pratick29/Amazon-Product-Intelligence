import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Deal Simulator", page_icon="🧪", layout="wide")
st.title("🧪 Deal Simulator (What-if Analysis)")
st.caption("Simulate price & discount changes and see how Value Score and segment recommendation change.")

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

# ------------------
# Select product
# ------------------
products = sorted(df["product_name"].astype(str).unique().tolist())
product = st.selectbox("Select a product to simulate", products)

row = df[df["product_name"] == product].iloc[0]

st.subheader("Original Product")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Actual Price", f"₹{row['actual_price']:.0f}")
c2.metric("Discounted Price", f"₹{row['discounted_price']:.0f}")
c3.metric("Discount %", f"{row['discount_percentage']:.1f}%")
c4.metric("Value Score", f"{row['value_score']:.1f}")

st.write(f"**Segment:** {row.get('segment_name','—')}")
st.divider()

# ------------------
# Simulation Controls
# ------------------
st.subheader("Simulate New Deal")

new_actual = st.number_input("New Actual Price (₹)", min_value=1.0, value=float(row["actual_price"]))
new_discounted = st.number_input("New Discounted Price (₹)", min_value=1.0, value=float(row["discounted_price"]))

if new_actual <= 0 or new_discounted <= 0:
    st.stop()

new_discount_pct = (1 - new_discounted / new_actual) * 100
new_discount_pct = max(0.0, min(100.0, new_discount_pct))

# ------------------
# Recompute Value Score (same method as notebook)
# ------------------
# We simulate using dataset scale to remain consistent
price_min, price_max = df["discounted_price"].min(), df["discounted_price"].max()
disc_min, disc_max = df["discount_percentage"].min(), df["discount_percentage"].max()

def safe_norm(x, minv, maxv):
    if maxv == minv:
        return 0.5
    return (x - minv) / (maxv - minv)

# price component: lower discounted price -> higher score
price_component = 1 - safe_norm(new_discounted, price_min, price_max)

# discount component: higher discount -> higher score
discount_component = safe_norm(new_discount_pct, disc_min, disc_max)

new_value_score = (0.6 * discount_component + 0.4 * price_component) * 100

# ------------------
# Decision / segment suggestion (rule-based)
# ------------------
trust = float(row["trust_score"])
pop = float(row["popularity_score"])

if new_value_score >= 80 and trust >= 70:
    new_segment = "Best Deals (simulated)"
elif new_discount_pct >= 60 and trust < 40:
    new_segment = "Discount Trap (simulated)"
elif trust >= 80 and pop < 25:
    new_segment = "Hidden Gems (simulated)"
elif new_discounted > row["discounted_price"] * 1.2 and trust >= 70:
    new_segment = "Premium Picks (simulated)"
else:
    new_segment = "Balanced / Market"

# ------------------
# Show results
# ------------------
st.divider()
st.subheader("Simulation Result")

a, b, c, d = st.columns(4)
a.metric("New Discount %", f"{new_discount_pct:.1f}%")
b.metric("New Value Score", f"{new_value_score:.1f}")
c.metric("Trust Score", f"{trust:.1f}")
d.metric("Popularity Score", f"{pop:.1f}")

if new_value_score > row["value_score"]:
    st.success(f"📈 Deal improved. New recommended segment: **{new_segment}**")
elif new_value_score < row["value_score"]:
    st.warning(f"📉 Deal weakened. New recommended segment: **{new_segment}**")
else:
    st.info(f"Deal quality unchanged. New recommended segment: **{new_segment}**")
