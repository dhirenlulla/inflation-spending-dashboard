# app.py - Fully Robust Enhanced Streamlit Dashboard

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

# --- File paths ---
DATA_DIR = "data"
INFLATION_FILE = f"{DATA_DIR}/india_inflation_clean.csv"
SPENDING_FILE = f"{DATA_DIR}/spending_clean.csv"

# --- Load data ---
@st.cache_data
def load_data():
    inflation = pd.read_csv(INFLATION_FILE)
    spending = pd.read_csv(SPENDING_FILE)
    
    # Ensure all spending columns are numeric (ignore year)
    spending.iloc[:, 1:] = spending.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    
    # Merge datasets for correlation analysis
    merged = pd.merge(spending, inflation, on="year", how="inner")
    return inflation, spending, merged

inflation, spending, merged = load_data()

# --- App Title ---
st.title("📊 India Inflation & Household Spending Dashboard")

# --- Sidebar Options ---
st.sidebar.header("Options")
view = st.sidebar.selectbox(
    "Select view:",
    [
        "Inflation Trend",
        "Spending Snapshot",
        "Multi-category Spending",
        "Inflation vs Spending",
        "Inflation-Adjusted Spending"
    ]
)

# --- Inflation Trend ---
if view == "Inflation Trend":
    st.subheader("Inflation Over Time")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=inflation, x="year", y="inflation_pct", marker="o", ax=ax)
    ax.set_ylabel("Inflation (%)")
    ax.set_xlabel("Year")
    ax.set_title("India Inflation Trend (1960-Present)")
    st.pyplot(fig)

# --- Spending Snapshot (Single Year) ---
elif view == "Spending Snapshot":
    st.subheader("Household Spending Snapshot")
    
    year_selected = st.sidebar.slider(
        "Select Year",
        int(inflation['year'].min()),
        int(inflation['year'].max()),
        int(inflation['year'].max()),
        step=1
    )
    
    # Copy spending data and select numeric columns
    spending_year = spending.copy()
    spending_year['year'] = year_selected
    spending_numeric = spending_year.select_dtypes(include='number').drop(columns='year', errors='ignore')
    
    # Build 2-column DataFrame
    plot_df = pd.DataFrame({
        "Category": spending_numeric.columns,
        "Average Spending": spending_numeric.iloc[0].values
    })
    
    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(data=plot_df, x='Category', y='Average Spending', ax=ax)
    ax.set_ylabel("Average Spending (Yearly Units)")
    ax.set_xlabel("Category")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# --- Multi-category Spending Trends ---
elif view == "Multi-category Spending":
    st.subheader("Spending Trends Over Time")
    
    categories = st.sidebar.multiselect(
        "Select categories:",
        spending.columns[1:],  # Exclude 'year'
        default=list(spending.columns[1:3])
    )
    
    if categories:
        fig, ax = plt.subplots(figsize=(12,6))
        for cat in categories:
            sns.lineplot(data=spending, x='year', y=cat, marker="o", ax=ax, label=cat)
        ax.set_ylabel("Average Spending (Yearly Units)")
        ax.set_xlabel("Year")
        ax.set_title("Spending Trends Over Years")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Please select at least one category.")

# --- Inflation vs Spending Correlation ---
elif view == "Inflation vs Spending":
    st.subheader("Correlation Between Inflation & Spending")
    corr = merged.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

# --- Inflation-Adjusted Spending Projection ---
elif view == "Inflation-Adjusted Spending":
    st.subheader("Inflation-Adjusted Spending Projection (from latest year snapshot)")
    
    latest_year = inflation['year'].max()
    
    # Select numeric columns only for latest spending row
    latest_spending = spending.select_dtypes(include='number').iloc[-1]
    categories = latest_spending.index.drop('year', errors='ignore')
    
    # Build inflation-adjusted dataset
    records = []
    for _, row in inflation.iterrows():
        year = row['year']
        cpi_ratio = row['cpi_index'] / inflation[inflation['year']==latest_year]['cpi_index'].values[0]
        for cat in categories:
            adj_spend = latest_spending[cat] * cpi_ratio
            records.append({'year': year, 'Category': cat, 'Inflation-Adjusted Spending': adj_spend})
    
    proj_df = pd.DataFrame(records)
    
    selected_cats = st.sidebar.multiselect(
        "Select categories to plot:",
        categories,
        default=list(categories[:3])
    )
    
    if selected_cats:
        fig, ax = plt.subplots(figsize=(12,6))
        for cat in selected_cats:
            sns.lineplot(
                data=proj_df[proj_df['Category']==cat],
                x='year',
                y='Inflation-Adjusted Spending',
                marker="o",
                ax=ax,
                label=cat
            )
        ax.set_ylabel("Spending (Yearly Units, Inflation-Adjusted)")
        ax.set_xlabel("Year")
        ax.set_title("Inflation-Adjusted Spending Projection")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Select at least one category for projection.")