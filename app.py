import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJgDBfNelXYmNKyNTI98jZQtFOZRVEQlPjFrHznNfsXGigWCwtkZymom7XM0BW4FH6MiCzqUSE3zXB/pub?output=csv"

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    return df

df = load_data()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("💰 Personal Finance Dashboard")

st.caption("Live data from Google Sheets")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Filters")

accounts = st.sidebar.multiselect(
    "Account",
    df["Account"].dropna().unique(),
    default=df["Account"].dropna().unique()
)

categories = st.sidebar.multiselect(
    "Category",
    df["Category"].dropna().unique(),
    default=df["Category"].dropna().unique()
)

filtered_df = df[
    df["Account"].isin(accounts)
    & df["Category"].isin(categories)
]

# ---------------------------------------------------
# KPI'S
# ---------------------------------------------------

income = filtered_df.loc[
    filtered_df["Amount"] > 0,
    "Amount"
].sum()

spending = abs(filtered_df.loc[
    filtered_df["Amount"] < 0,
    "Amount"
].sum())

net = income - spending

transactions = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Income", f"£{income:,.2f}")
col2.metric("Spending", f"£{spending:,.2f}")
col3.metric("Net Cashflow", f"£{net:,.2f}")
col4.metric("Transactions", transactions)

st.divider()

# ---------------------------------------------------
# CATEGORY SPEND
# ---------------------------------------------------

spend_df = (
    filtered_df[filtered_df["Amount"] < 0]
    .groupby("Category")["Amount"]
    .sum()
    .abs()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    spend_df,
    x="Category",
    y="Amount",
    title="Spending by Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# MONTHLY TREND
# ---------------------------------------------------

filtered_df["Month"] = (
    filtered_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    filtered_df
    .groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Cashflow"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# CATEGORY PIE
# ---------------------------------------------------

fig3 = px.pie(
    spend_df,
    names="Category",
    values="Amount",
    title="Spending Breakdown"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------

st.subheader("Transactions")

st.dataframe(
    filtered_df.sort_values(
        "Date",
        ascending=False
    ),
    use_container_width=True
)
