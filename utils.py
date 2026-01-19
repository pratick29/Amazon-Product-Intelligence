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
        padding:6px 10px;
        border-radius:999px;
        font-size:12px;
        font-weight:600;">
        {segment}
    </span>
    """

def product_card(row):
    return f"""
    <div style="
        border:1px solid #e5e7eb;
        border-radius:16px;
        padding:14px;
        margin-bottom:12px;
        background:white;
        box-shadow:0 1px 3px rgba(0,0,0,0.08);">

        <div style="font-size:16px;font-weight:700;">{row['product_name']}</div>
        <div style="color:#6b7280;margin:6px 0;">{row['main_category']}</div>

        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <div>💰 <b>₹{row['discounted_price']:.0f}</b></div>
            <div>🔻 <b>{row['discount_percentage']:.1f}%</b></div>
            <div>⭐ <b>{row['rating']:.2f}</b></div>
        </div>

        <div style="margin-top:10px;">
            {segment_badge(row.get("segment_name","—"))}
        </div>
    </div>
    """
