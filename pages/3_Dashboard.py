import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from utils.transaction import get_dashboard_summary, get_transactions
from utils.budget import get_budget_progress
from utils.ui import apply_theme, sidebar

st.set_page_config(page_title="Dashboard | FinTrack", page_icon="📊", layout="wide")
if "logged_in" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()
apply_theme()
user = st.session_state.user
user_id = user[0]
sidebar(user)
summary, rows = get_dashboard_summary(user_id), get_transactions(user_id)
df = pd.DataFrame(rows, columns=["ID", "Date", "Type", "Category", "Description", "Amount"]) if rows else pd.DataFrame(columns=["ID", "Date", "Type", "Category", "Description", "Amount"])

st.title(f"Good to see you, {user[1].split()[0]}")
st.caption("A clear view of your money, budgets, and next actions.")
a, b, c, d = st.columns(4)
a.metric("Total income", f"RM {summary['income']:,.2f}")
b.metric("Total expenses", f"RM {summary['expense']:,.2f}")
c.metric("Current balance", f"RM {summary['balance']:,.2f}")
d.metric("Transactions", summary['transactions'])

monthly = df[df["Date"].astype(str).str.startswith(date.today().strftime("%Y-%m"))] if not df.empty else df
month_income = monthly.loc[monthly.Type == "Income", "Amount"].sum()
month_expense = monthly.loc[monthly.Type == "Expense", "Amount"].sum()
savings = month_income - month_expense
rate = (savings / month_income * 100) if month_income else 0
st.divider()
left, right = st.columns([1.15, 1])
with left:
    st.subheader("Monthly savings")
    st.metric("This month", f"RM {savings:,.2f}", f"{rate:.1f}% savings rate")
    st.progress(min(max(rate, 0), 100) / 100, text=f"{rate:.0f}% of monthly income retained")
    if rate >= 20:
        st.success("Great pace — you are saving at least 20% of this month's income.")
    elif month_income:
        st.info("Aim for a 20% savings rate by trimming one flexible expense category.")
    else:
        st.info("Add income transactions to calculate your monthly savings rate.")
with right:
    st.subheader("Financial health")
    if summary["income"] == 0:
        score, label = 0, "Needs data"
    else:
        ratio = summary["expense"] / summary["income"]
        score = round(max(0, min(100, 100 - ratio * 65 + (15 if summary["balance"] > 0 else 0))))
        label = "Strong" if score >= 75 else "Fair" if score >= 50 else "Needs attention"
    st.metric(label, f"{score}/100")
    st.progress(score / 100)
    st.caption("Based on your total spending ratio and current balance.")

st.divider()
col1, col2 = st.columns([1.25, 1])
with col1:
    st.subheader("Recent activity")
    if df.empty:
        st.info("Your latest transactions will appear here.")
    else:
        activity = df.head(6).copy()
        activity["Amount"] = activity.apply(lambda x: f"{'+' if x.Type == 'Income' else '-'} RM {x.Amount:,.2f}", axis=1)
        st.dataframe(activity[["Date", "Category", "Description", "Amount"]], hide_index=True, use_container_width=True)
with col2:
    st.subheader("Top spending")
    expenses = df[df.Type == "Expense"]
    if expenses.empty:
        st.info("Expense categories will appear after you add spending.")
    else:
        top = expenses.groupby("Category", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False).head(5)
        st.plotly_chart(px.bar(top, x="Amount", y="Category", orientation="h", color="Amount", color_continuous_scale="Blues", text_auto=".0f"), use_container_width=True, config={"displayModeBar": False})

st.divider()
st.subheader("Budget progress — this month")
progress = get_budget_progress(user_id)
if not progress:
    st.info("Set category budgets in the Budget Planner to see live progress.")
else:
    alerts = []
    for category, limit, spent in progress:
        percent = (spent / limit * 100) if limit else 0
        st.write(f"**{category}**  ·  RM {spent:,.2f} of RM {limit:,.2f}")
        st.progress(min(percent, 100) / 100, text=f"{percent:.0f}% used")
        if percent >= 100: alerts.append(f"{category} budget exceeded")
        elif percent >= 80: alerts.append(f"{category} is near its limit")
    if st.session_state.get("budget_alerts", True) and alerts:
        st.warning(" • ".join(alerts))
