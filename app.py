import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

CSV_URL = "YOUR_GOOGLE_SHEET_CSV_URL_HERE"

@st.cache_data
def load_data():

    df = pd.read_csv(CSV_URL)

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    df["ABS Amount"] = pd.to_numeric(
        df["ABS Amount"],
        errors="coerce"
    )

    return df

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Filters")

accounts = st.sidebar.multiselect(
    "Account",
    df["Account"].unique(),
    default=df["Account"].unique()
)

categories = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

df = df[
    (df["Account"].isin(accounts))
    &
    (df["Category"].isin(categories))
]

# ==========================================
# HEADER
# ==========================================

st.title("💰 Personal Finance Dashboard")

# ==========================================
# KPI CARDS
# ==========================================

income = df[df["Amount"] > 0]["Amount"].sum()

spending = abs(
    df[df["Amount"] < 0]["Amount"].sum()
)

net_cashflow = income - spending

transactions = len(df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Income", f"£{income:,.2f}")
c2.metric("Spending", f"£{spending:,.2f}")
c3.metric("Net Cashflow", f"£{net_cashflow:,.2f}")
c4.metric("Transactions", transactions)

st.divider()

# ==========================================
# CATEGORY SPENDING
# ==========================================

spend_by_category = (
    df[df["Amount"] < 0]
    .groupby("Category")["ABS Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig1 = px.bar(
    spend_by_category,
    x="Category",
    y="ABS Amount",
    title="Spending By Category"
)

# ==========================================
# P&L CATEGORY
# ==========================================

spend_by_pl = (
    df[df["Amount"] < 0]
    .groupby("P&L Category")["ABS Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.pie(
    spend_by_pl,
    names="P&L Category",
    values="ABS Amount",
    title="P&L Breakdown"
)

# ==========================================
# FIXED VS NON FIXED
# ==========================================

fixed_df = (
    df[df["Amount"] < 0]
    .groupby("Non/Fixed")["ABS Amount"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    fixed_df,
    names="Non/Fixed",
    values="ABS Amount",
    title="Fixed vs Non Fixed"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# WEEKLY SPEND
# ==========================================

weekly = (
    df[df["Amount"] < 0]
    .groupby("WeekNum")["ABS Amount"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    weekly,
    x="WeekNum",
    y="ABS Amount",
    markers=True,
    title="Weekly Spending"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# MERCHANT ANALYSIS
# ==========================================

merchant_spend = (
    df[df["Amount"] < 0]
    .groupby("Merchant")["ABS Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    merchant_spend,
    x="Merchant",
    y="ABS Amount",
    title="Top Merchants"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==========================================
# TRANSACTIONS
# ==========================================

st.subheader("Transactions")

st.dataframe(
    df.sort_values(
        "Date",
        ascending=False
    ),
    use_container_width=True
)
