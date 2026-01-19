# 🛒 Amazon Product Intelligence Dashboard  
### EDA + Value/Trust/Popularity Scoring + Segmentation + Streamlit Frontend

An end-to-end data analytics + product intelligence project that transforms raw Amazon marketplace data into **actionable business insights**.

This project goes beyond traditional EDA by building a **Product Intelligence System** that helps identify:

✅ Best Deals (high value + high trust)  
⚠️ Discount Traps (high discounts but low trust)  
💎 Hidden Gems (high trust but low visibility)  
🏆 Premium Picks / Market Leaders (high popularity & stable trust)  

It also includes an interactive **Streamlit dashboard** with product search, filters, drill-down views, recommendations, and review intelligence.

---

## 📌 Live Demo (Deployed App)

🔗 **Streamlit Dashboard:**  
> Add your deployment link here  
`https://your-app-name.streamlit.app`

---

## 🎯 Business Problem

Amazon has a huge catalog of products with different price points, discounts, and customer feedback.

However:
- Not all discounts represent genuine value
- Ratings alone can be misleading (low review count bias)
- Some products appear attractive but are risky (fake/broken complaints)

### ✅ Goal
Build a data-driven system to support:
- promotion strategy  
- pricing intelligence  
- product quality monitoring  
- catalog segmentation  

---

## 🧠 Project Highlights

✅ Cleaned and preprocessed messy marketplace data (₹ symbols, commas, %, missing values)  
✅ Built **three decision metrics**:
- **Value Score**: Deal quality based on discount + affordability  
- **Trust Score**: Weighted rating to account for review reliability  
- **Popularity Score**: Demand proxy using rating_count  

✅ Segmented products using **K-Means clustering**  
✅ Built an interactive Streamlit app with:
- product explorer
- product drill-down
- category insights
- recommendation engine
- NLP review intelligence
- what-if deal simulator
- product comparison tool

---

## 📊 Dashboard Pages & Features

### 🔍 Product Explorer
- Search by product name
- Filter by category, segment, rating, discount, price range
- Shows **deal badges** + **segment badges**
- Table + downloadable CSV

### 📌 Product Details (Drill-down)
- Displays complete product profile:
  - pricing, discount, ratings
  - Value/Trust/Popularity scores
  - segment recommendation
  - review snippets

### 📊 Category Intelligence
- Category-level KPIs:
  - avg discount
  - avg rating
  - avg value/trust
  - category distribution

### 🤝 Recommendation Engine
- Recommends products based on:
  - budget (₹)
  - category
  - minimum rating
  - preference: best overall / best value / most trusted / most popular

### 🧾 Review Intelligence (NLP)
- Sentiment scoring (VADER)
- Risk keyword flags (fake, broken, duplicate, waste, refund...)
- Highlights risky products with negative sentiment

### ⚖️ Compare Products
- Side-by-side comparison of two products
- Winner suggestion based on weighted intelligence score

### 🧪 Deal Simulator
- What-if simulation:
  - adjust actual price & discounted price
  - see updated discount %
  - recompute Value Score
  - segment recommendation changes accordingly

---

## 🧰 Tech Stack

- **Python**
- **Pandas, NumPy** (data processing)
- **Matplotlib / Seaborn** (visualizations)
- **Scikit-learn** (K-Means clustering)
- **NLTK (VADER Sentiment)** (review sentiment)
- **Streamlit** (frontend dashboard)

---

## 📂 Dataset

**Source:** Kaggle Amazon Sales Dataset  
🔗 https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset

Dataset includes:
- product metadata (category, price, discount)
- customer ratings & review counts
- review text (title/content)

---

## 🏗️ Project Structure

```bash
Amazon-Product-Intelligence/
│
├── notebooks/
│   └── amazon_product_intelligence.ipynb
│
├── outputs/
│   └── scored_segmented_products.csv
│
├── pages/
│   ├── 1_🔍_Product_Explorer.py
│   ├── 2_📌_Product_Details.py
│   ├── 3_📊_Category_Intelligence.py
│   ├── 4_🧠_Insights_&_Explainability.py
│   ├── 5_🤝_Recommendation_Engine.py
│   ├── 6_🧾_Review_Intelligence.py
│   ├── 7_⚖️_Compare_Products.py
│   └── 8_🧪_Deal_Simulator.py
│
├── app.py
├── requirements.txt
└── README.md
