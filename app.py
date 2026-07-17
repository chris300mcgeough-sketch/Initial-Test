import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta

st.set_page_config(
    page_title="Finance Dashboard",
    layout="wide"
)

df = pd.read_csv(
    "finance_transactions.csv"
)

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)

today = df["Date"].max()

# --------------------
# Metric Functions
# --------------------

def spend(x):

    return abs(
        x.loc[
            x["Amount"] < 0,
            "Amount"
        ].sum()
    )

def period_value(dataset, days):

    return spend(
        dataset[
            dataset["Date"]
            >= today - timedelta(days=days)
        ]
    )

def prev_period(dataset, start, end):

    return spend(
        dataset[
            (dataset["Date"]
             >= today - timedelta(days=end))
            &
            (dataset["Date"]
             < today - timedelta(days=start))
        ]
    )

def arrow(curr, prev):

    if curr < prev:
        return "🟢⬇"
    elif curr > prev:
        return "🔴⬆"
    else:
        return "⚪"

# --------------------
# Summary
# --------------------

cats = {
    "Total": df,
    "Fixed": df[df["Non/Fixed"]=="Fixed"],
    "Not Fixed": df[df["Non/Fixed"]=="Non Fixed"],
    "Lifestyle":
        df[df["P&L Category"]=="Lifestyle"],
    "Variable":
        df[df["Non/Fixed"]=="Non Fixed"]
}

rows = []

for label,data in cats.items():

    l7 = period_value(data,7)
    p7 = prev_period(data,7,14)

    rows.append([
        label,
        f"£{l7:,.2f}",
        arrow(l7,p7)
    ])

summary = pd.DataFrame(
    rows,
    columns=[
        "Category",
        "Last 7",
        "Trend"
    ]
)

st.title(
    "💰 Personal Finance Dashboard"
)

st.dataframe(
    summary,
    use_container_width=True
)

# --------------------
# Pareto
# --------------------

pareto = (
    df[df["Amount"] < 0]
    .groupby("Category")
    ["ABS Amount"]
    .sum()
    .sort_values(ascending=False)
)

cum = (
    pareto.cumsum()
    / pareto.sum()
    *100
)

fig = go.Figure()

fig.add_bar(
    x=pareto.index,
    y=pareto.values,
    name="Spend"
)

fig.add_scatter(
    x=pareto.index,
    y=cum,
    mode="lines+markers",
    yaxis="y2",
    name="Cumulative%"
)

fig.update_layout(
    title="YTD Spending Pareto",
    yaxis2=dict(
        overlaying="y",
        side="right",
        range=[0,100]
    )
)

# --------------------
# Monthly
# --------------------

monthly = (
    df.groupby(
        df["Date"].dt.strftime("%Y-%m")
    )
    ["ABS Amount"]
    .sum()
)

fig2 = px.bar(
    monthly,
    title="Monthly Spend"
)

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------
# Transactions
# --------------------

st.subheader(
    "Transaction Explorer"
)

st.dataframe(
    df.sort_values(
        "Date",
        ascending=False
    ),
    use_container_width=True
)
