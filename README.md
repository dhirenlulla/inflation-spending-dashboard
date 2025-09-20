# India Inflation & Household Spending Dashboard

An interactive **Streamlit dashboard** that analyzes India's **inflation trends** and **household spending patterns** using historical datasets. Explore spending snapshots, trends, correlations, and inflation-adjusted projections.

---

## 📂 Project Structure

inflation_spending_project/
├── data/
│ ├── india_inflation_clean.csv # Cleaned CPI & inflation data
│ └── spending_clean.csv # Cleaned household spending data
├── notebooks/
│ └── analysis.ipynb # Jupyter notebook for data exploration
├── app.py # Streamlit dashboard
└── README.md

---

## 🛠️ Features

1. **Inflation Trend** – Yearly inflation (%) from 1960 to present.
2. **Spending Snapshot** – Average household spending for a selected year.
3. **Multi-category Spending Trends** – Compare multiple spending categories over time.
4. **Inflation vs Spending Correlation** – Visualize which spending categories are most correlated with inflation.
5. **Inflation-Adjusted Spending Projection** – See how spending would have changed historically using CPI.

---

## 💾 Datasets

- **World Bank CPI & Inflation** – `india_inflation_clean.csv`
- **Household Spending (Kaggle dataset)** – `spending_clean.csv`

Place both files inside the `data/` folder.

---

## 🚀 How to Run Locally

1. Install required packages:

```bash
pip install streamlit pandas matplotlib seaborn
```

2. Run the Streamlit dashboard:

```bash
streamlit run app.py
```

3. The app will open in your default browser. Use the sidebar to interact with plots and select views.

**🌐 Hosted Version**

[Live Dashboard Link](https://inflation-spending-dashboard-mdeasyqrwhmcdcdgvzfqux.streamlit.app/)

**📈 Insights**

Inflation has fluctuated over decades, influencing household spending.

Spending categories like Groceries, Transport, and Rent show higher correlations with inflation.

Inflation-adjusted projections visualize historical spending changes if adjusted for CPI.

**📌 Author**

Dhiren Lulla – Data Science Enthusiast
