<div align="center">

# 🛒 RetailPulse — Retail Sales Analytics Dashboard

**A Power BI-style interactive dashboard in pure Python — 40,000 transactions, 9 cities, instant insights.**

![Python-3.10%2B](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Streamlit-App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Plotly-Charts](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) ![Pandas-Analysis](https://img.shields.io/badge/Pandas-Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Domain-Data%20Analytics](https://img.shields.io/badge/Domain-Data%20Analytics-F2C811?style=for-the-badge&logo=powerbi&logoColor=white)

`Data Analysis · Business Intelligence`

</div>

---

![RETAIL-SALES-ANALYTICS-DASHBOARD](assets/screenshot.png)

## 📌 Problem Statement

Retail managers need one place to see revenue, profit and customer behaviour across cities, categories and channels — and spot seasonality early.

## ✨ Key Features

- Sidebar **slicers**: date range, region, category, channel
- KPI cards with **YoY growth**: revenue, profit, orders, AOV, margin
- Monthly trend with **3-month moving average** (festive-season peaks)
- Sunburst revenue mix, city ranking, **day × hour heatmap**, channel share
- Top-products table with margin bars and **auto-generated insights**
- Export filtered data to CSV

## 🏗️ Architecture

```mermaid
flowchart LR
    A[Sales CSV / Generator] --> B[Pandas Cleaning]
    B --> C[Filters & Slicers]
    C --> D[KPIs + YoY]
    C --> E[Trends & Heatmaps]
    C --> F[Auto Insights]
    C --> G[CSV Export]
```

## ⚙️ How It Works

1. Synthetic sales with realistic seasonality (Oct–Nov festive peak), weekend lift, growth trend, discounts and category margins.
2. Pandas `groupby`, `resample` and `pivot_table` power every visual; filters cascade to all charts.
3. Insights are computed from the filtered data (most profitable category, top city, peak month, discount impact on margin).

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| ML / Logic | pandas, numpy |
| UI & Visualisation | Streamlit, Plotly |

## 📁 Project Structure

```
RETAIL-SALES-ANALYTICS-DASHBOARD/
├── app.py             # Dashboard layout, KPIs, charts, insights
├── data.py            # Synthetic multi-city transaction generator
├── assets/              # screenshots
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

```bash
git clone https://github.com/PreciousBharath/RETAIL-SALES-ANALYTICS-DASHBOARD.git
cd RETAIL-SALES-ANALYTICS-DASHBOARD
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

> The project ships with a realistic built-in demo dataset, so it runs out of the box with no downloads or API keys.

## 🗺️ Roadmap

- [ ] Sales forecasting with Prophet
- [ ] Connect to MySQL / Google Sheets
- [ ] Scheduled PDF report emails

## 👨‍💻 Author

**Bharath** — Software Developer · Project Engineer · Technical Trainer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-connectbharath-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/connectbharath)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://itsbharathportfolio.netlify.app)
[![GitHub](https://img.shields.io/badge/GitHub-PreciousBharath-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PreciousBharath)

⭐ If this project helped you, please give it a star!

## 📄 License

Released under the [MIT License](LICENSE).
