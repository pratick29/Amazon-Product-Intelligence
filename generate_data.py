import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import nltk
from textblob import TextBlob
import re

df = pd.read_csv("data/amazon.csv")

def clean_price(x):
    if pd.isna(x):
        return np.nan
    x = str(x).replace("₹", "").replace(",", "").strip()
    return pd.to_numeric(x, errors="coerce")

df["actual_price"] = df["actual_price"].apply(clean_price)
df["discounted_price"] = df["discounted_price"].apply(clean_price)
df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "")
    .str.strip()
)
df["discount_percentage"] = pd.to_numeric(df["discount_percentage"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "")
    .str.strip()
)
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")
df = df.drop_duplicates()
df = df.dropna(subset=["actual_price", "discounted_price", "discount_percentage"])
df["rating"] = df["rating"].fillna(df["rating"].median())
df["rating_count"] = df["rating_count"].fillna(0)

df["discount_amount"] = df["actual_price"] - df["discounted_price"]
df["discount_ratio"] = df["discount_amount"] / df["actual_price"]
df["price_bucket"] = pd.cut(df["discounted_price"], bins=5, labels=[
    "Very Low", "Low", "Medium", "High", "Very High"
])
df["main_category"] = df["category"].astype(str).apply(lambda x: x.split("|")[0])

df["popularity_score"] = (df["rating_count"] - df["rating_count"].min()) / (
    df["rating_count"].max() - df["rating_count"].min()
) * 100

m = df["rating_count"].quantile(0.60)
C = df["rating"].mean()

def weighted_rating(row):
    v = row["rating_count"]
    R = row["rating"]
    return (v/(v+m))*R + (m/(v+m))*C

df["weighted_rating"] = df.apply(weighted_rating, axis=1)
df["trust_score"] = (df["weighted_rating"] - df["weighted_rating"].min()) / (
    df["weighted_rating"].max() - df["weighted_rating"].min()
) * 100

price_component = 1 - (df["discounted_price"] - df["discounted_price"].min()) / (
    df["discounted_price"].max() - df["discounted_price"].min()
)

discount_component = (df["discount_percentage"] - df["discount_percentage"].min()) / (
    df["discount_percentage"].max() - df["discount_percentage"].min()
)

df["value_score"] = (0.6 * discount_component + 0.4 * price_component) * 100

features = df[["value_score", "trust_score", "popularity_score"]].copy()

scaler = StandardScaler()
X = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=5, random_state=42)
df["segment"] = kmeans.fit_predict(X)

segment_map = {
    0: "Best Deals",
    1: "Discount Trap",
    2: "Hidden Gems",
    3: "Market Leaders",
    4: "Premium Picks"
}

df["segment_name"] = df["segment"].map(segment_map)

# ---------------------------
# NLP Features: Sentiment Analysis and Keyword Alerts
# ---------------------------
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def get_sentiment(text):
    if pd.isna(text):
        return "Neutral"
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def has_complaint_keywords(text):
    if pd.isna(text):
        return False
    keywords = ["fake", "broken", "poor quality", "waste", "duplicate", "defective", "not working"]
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in keywords)

df["sentiment"] = df["review_content"].apply(get_sentiment)
df["complaint_risk"] = df["review_content"].apply(has_complaint_keywords)

# Save the full scored and segmented dataset
df.to_csv("outputs/scored_segmented_products.csv", index=False)

print("Data generated and saved to outputs/scored_segmented_products.csv")
