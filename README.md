# FUTURE_DS_01-
Sales analysis of 500K+ real e-commerce transactions — revenue trends, top products, customer behaviour &amp; business recommendations. Built with Python &amp; Matplotlib.
# 🛒 Online Retail Sales Analysis — Business Intelligence Dashboard

A complete, client-ready sales analytics project built on real e-commerce transaction data.  
Covers data cleaning, KPI analysis, trend identification, customer segmentation, and actionable business recommendations.

---

## 📊 Dashboard Preview

| Page 1 — KPIs, Revenue Trend, Top Products & Markets | Page 2 — Customer Behaviour & Order Patterns |
|---|---|
| ![Dashboard Page 1](retail_dashboard_page1.png) | ![Dashboard Page 2](retail_dashboard_page2.png) |

---

## 📁 Project Files

| File | Description |
|---|---|
| `online_retail.csv` | Raw dataset (541,909 rows) |
| `retail_analysis.py` | Full Python analysis & dashboard script |
| `retail_dashboard_page1.png` | Dashboard — KPIs, trends, products, markets |
| `retail_dashboard_page2.png` | Dashboard — customer & order behaviour |
| `retail_insights_report.txt` | Written business insights & recommendations |

---

## 🗃️ Dataset

**Source:** [Online Retail Dataset — Kaggle](https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset)  
**Period:** December 2010 – December 2011  
**Records after cleaning:** 397,884 transactions

**Columns:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`

---

## 🧹 Data Cleaning Steps

- Removed rows with missing `CustomerID` (anonymous transactions)
- Removed rows with missing `Description`
- Filtered out cancelled orders (`InvoiceNo` starting with `"C"`)
- Removed negative/zero `Quantity` and `UnitPrice` values
- Parsed `InvoiceDate` to datetime; extracted `YearMonth`, `Month`, `Year`, `DayOfWeek`
- Created `Revenue` column: `Quantity × UnitPrice`

---

## 📈 Key KPIs

| Metric | Value |
|---|---|
| Total Revenue | **£8,911,407.90** |
| Total Orders | **18,532** |
| Unique Customers | **4,338** |
| Unique Products | **3,665** |
| Average Order Value | **£480.87** |

---

## 🔍 Key Business Insights

### 1. Strong Q4 Seasonality
Revenue peaks sharply in **November (£1.2M)** driven by Christmas/holiday gifting demand.  
Q1 (Jan–Feb) shows a consistent post-holiday dip — cash flow planning is critical.

### 2. Home Décor & Giftware Drive Revenue
The top 10 products are almost entirely home décor and novelty gift items.  
Classic **80/20 rule** applies — a small SKU set drives disproportionate revenue.

### 3. High UK Dependency (>80% Revenue)
The UK dominates revenue. **Netherlands, Ireland, Germany, and France** are the next biggest markets but remain small — significant international growth potential exists.

### 4. Many One-Time Buyers
Most customers order **1–2 times**. Improving customer retention is the highest-ROI opportunity.  
The top 10 customers alone contribute a significant share of total revenue.

### 5. B2B Wholesale Pattern
**Thursday and Tuesday** are peak revenue days; Sunday is nearly zero.  
This confirms a wholesale/B2B purchasing pattern (retailers restocking for weekend sales).

---

## ✅ Actionable Recommendations

| # | Recommendation | Impact |
|---|---|---|
| 1 | **Seasonal campaigns** — Start October email/ad push; pre-bundle holiday gift sets | High |
| 2 | **Loyalty programme** — Follow-up offers 30–60 days post first purchase | High |
| 3 | **International expansion** — Localised catalogues for Netherlands, Germany, France | Medium |
| 4 | **VIP customer management** — Personally manage top 50 customers by revenue | Medium |
| 5 | **SKU rationalisation** — Discontinue/bundle slow movers; focus on top 100 SKUs | Medium |
| 6 | **Midweek promotions** — Flash sales Monday/Tuesday to smooth order volume | Low |

---

## 🛠️ Tools Used

- **Python 3** — pandas, matplotlib
- **Libraries:** `pandas`, `matplotlib`, `warnings`

---

## 🚀 How to Run

```bash
# Install dependencies
pip install pandas matplotlib

# Run analysis
python retail_analysis.py
```

Outputs:
- `retail_dashboard_page1.png`
- `retail_dashboard_page2.png`
- `retail_insights_report.txt` (printed to console and saved)

---

## 👩‍💻 About This Project

This project was completed as part of a **Future Interns Data Analytics Internship Task**.  
The goal was to perform real-world business sales analysis — cleaning raw data, identifying trends, and presenting findings as a client-ready report with actionable recommendations.

---

*Built with Python · Data sourced from Kaggle · Analysis by Hajira*
