import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Download VADER lexicon
nltk.download("vader_lexicon")

# Load the existing data
df = pd.read_csv("outputs/scored_segmented_products.csv")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if pd.isna(text):
        return 0
    text = str(text)
    return sia.polarity_scores(text)["compound"]

# Add sentiment score
df["sentiment_score"] = df["review_content"].apply(get_sentiment)

# Risk keyword flags
risk_words = [
    "fake", "broken", "waste", "duplicate", "bad", "poor", "damage",
    "defective", "fraud", "worst", "return", "refund"
]

def risk_flag(text):
    if pd.isna(text):
        return 0
    text = str(text).lower()
    for w in risk_words:
        if re.search(rf"\b{w}\b", text):
            return 1
    return 0

# Add risk flag
df["risk_flag"] = df["review_content"].apply(risk_flag)

# Save back to CSV
df.to_csv("outputs/scored_segmented_products.csv", index=False)

print("NLP columns added successfully!")
print(f"Total products: {len(df)}")
print(f"Risk flagged products: {int(df['risk_flag'].sum())}")
print(f"Average sentiment: {df['sentiment_score'].mean():.3f}")
