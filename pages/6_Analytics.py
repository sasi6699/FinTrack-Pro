import calendar

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.transaction import get_transactions
from utils.ui import apply_theme, sidebar


def style_chart(chart):
    chart.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, .32)",
        font={"color": "#cbd5e1"},
        margin={"l": 12, "r": 12, "t": 36, "b": 12},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": .5},
    )
    chart.update_xaxes(gridcolor="rgba(148, 163, 184, .14)", linecolor="rgba(148, 163, 184, .18)")
    chart.update_yaxes(gridcolor="rgba(148, 163, 184, .14)", linecolor="rgba(148, 163, 184, .18)")
    return chart


def compact_filter_label(label, selected_values, all_values, all_label):
    """Summarise selections in the label instead of rendering a long tag list."""
    if not selected_values or len(selected_values) == len(all_values):
        return f"{label} · {all_label}"
    preview = ", ".join(map(str, selected_values[:2]))
    remaining = len(selected_values) - 2
    return f"{label} · {preview}{f' +{remaining} more' if remaining > 0 else ''}"


st.set_page_config(page_title="Analytics | FinTrack", page_icon="📈", layout="wide")
if "logged_in" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

apply_theme()
user = st.session_state.user
sidebar(user)

rows = get_transactions(user[0])
st.title("Financial analytics")
st.caption("Explore your cash flow across every year, month, category, and transaction type.")
st.markdown(
    """
    <style>
    [data-testid="stExpander"] { border: 1px solid rgba(96, 165, 250, .24); border-radius: 12px; background: rgba(20, 29, 45, .42); }
    [data-testid="stExpander"] details { padding: 0 .2rem; }
    [data-testid="stExpander"] [data-baseweb="tag"] { display: none !important; }
    [data-testid="stExpander"] [data-baseweb="select"] > div { min-height: 2.25rem; }
    [data-testid="stExpander"] [data-testid="stVerticalBlock"] { gap: .2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

if not rows:
    st.info("Add transactions to unlock your financial analytics.")
    st.stop()

df = pd.DataFrame(rows, columns=["ID", "Date", "Type", "Category", "Description", "Amount"])
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year.astype(str)
df["Month name"] = df["Date"].dt.month.map(lambda month: calendar.month_name[month])
df["Month number"] = df["Date"].dt.month

year_options = sorted(df["Year"].unique().tolist())
month_options = list(calendar.month_name[1:])
type_options = ["Income", "Expense"]
category_options = sorted(df["Category"].dropna().unique().tolist())
minimum_date = df["Date"].min().date()
maximum_date = df["Date"].max().date()

with st.expander("Filter analytics", expanded=True):
    year_column, month_column, date_column, type_column, category_column = st.columns([.85, 1.15, 1.35, 1, 1.65])
    selected_years = year_column.multiselect(
        compact_filter_label("Year", st.session_state.get("analytics_years", []), year_options, "All Years"),
        year_options, default=[], placeholder="All Years", key="analytics_years",
    )
    selected_months = month_column.multiselect(
        compact_filter_label("Month", st.session_state.get("analytics_months", []), month_options, "All Months"),
        month_options, default=[], placeholder="All Months", key="analytics_months",
    )
    selected_date_range = date_column.date_input("Date range", value=(minimum_date, maximum_date), min_value=minimum_date, max_value=maximum_date)
    selected_types = type_column.multiselect(
        compact_filter_label("Type", st.session_state.get("analytics_types", []), type_options, "All Types"),
        type_options, default=[], placeholder="All Types", key="analytics_types",
    )
    selected_categories = category_column.multiselect(
        compact_filter_label("Category", st.session_state.get("analytics_categories", []), category_options, "All Categories"),
        category_options, default=[], placeholder="All Categories", key="analytics_categories",
    )

selected_years = selected_years or year_options
selected_months = selected_months or month_options
selected_types = selected_types or type_options
selected_categories = selected_categories or category_options

if isinstance(selected_date_range, (tuple, list)) and len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
else:
    start_date = end_date = selected_date_range

filtered = df[
    df["Year"].isin(selected_years)
    & df["Month name"].isin(selected_months)
    & df["Type"].isin(selected_types)
    & df["Category"].isin(selected_categories)
    & df["Date"].dt.date.between(start_date, end_date)
].copy()

income = filtered.loc[filtered["Type"] == "Income", "Amount"].sum()
expense = filtered.loc[filtered["Type"] == "Expense", "Amount"].sum()
balance = income - expense

a, b, c, d = st.columns(4)
a.metric("Income", f"RM {income:,.2f}")
b.metric("Expenses", f"RM {expense:,.2f}")
c.metric("Net balance", f"RM {balance:,.2f}")
d.metric("Filtered transactions", f"{len(filtered):,}")

if filtered.empty:
    st.info("No transactions match the selected filters. Adjust one or more filters to see analytics.")
    st.stop()

left, right = st.columns(2)
with left:
    st.subheader("Income vs expenses")
    totals = filtered.groupby("Type", as_index=False)["Amount"].sum()
    comparison = px.bar(
        totals,
        x="Type",
        y="Amount",
        color="Type",
        text_auto=".2s",
        color_discrete_map={"Income": "#10b981", "Expense": "#ef4444"},
    )
    style_chart(comparison)
    st.plotly_chart(comparison, width="stretch", config={"displayModeBar": False})

with right:
    st.subheader("Expense breakdown")
    expenses = filtered[filtered["Type"] == "Expense"]
    if expenses.empty:
        st.info("No expense data matches the selected filters.")
    else:
        category_totals = expenses.groupby("Category", as_index=False)["Amount"].sum()
        breakdown = px.pie(category_totals, names="Category", values="Amount", hole=.48, color_discrete_sequence=px.colors.sequential.Blues_r)
        style_chart(breakdown)
        breakdown.update_traces(textfont={"color": "#f8fafc"})
        st.plotly_chart(breakdown, width="stretch", config={"displayModeBar": False})

st.subheader("Monthly cash flow")
monthly = filtered.copy()
monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)
monthly_trend = monthly.pivot_table(index="Month", columns="Type", values="Amount", aggfunc="sum", fill_value=0).reset_index()
for transaction_type in type_options:
    if transaction_type not in monthly_trend:
        monthly_trend[transaction_type] = 0
monthly_trend["Savings"] = monthly_trend["Income"] - monthly_trend["Expense"]
monthly_chart = px.line(monthly_trend, x="Month", y=["Income", "Expense", "Savings"], markers=True, color_discrete_map={"Income": "#10b981", "Expense": "#ef4444", "Savings": "#60a5fa"})
style_chart(monthly_chart)
st.plotly_chart(monthly_chart, width="stretch", config={"displayModeBar": False})

st.subheader("Yearly financial trend")
yearly_trend = filtered.pivot_table(index="Year", columns="Type", values="Amount", aggfunc="sum", fill_value=0).reset_index()
for transaction_type in type_options:
    if transaction_type not in yearly_trend:
        yearly_trend[transaction_type] = 0
yearly_trend["Savings"] = yearly_trend["Income"] - yearly_trend["Expense"]
yearly_chart = px.bar(yearly_trend, x="Year", y=["Income", "Expense", "Savings"], barmode="group", color_discrete_map={"Income": "#10b981", "Expense": "#ef4444", "Savings": "#60a5fa"})
style_chart(yearly_chart)
st.plotly_chart(yearly_chart, width="stretch", config={"displayModeBar": False})
