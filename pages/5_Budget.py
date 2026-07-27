import html

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.budget import get_budget_progress, save_budget
from utils.categories import EXPENSE_CATEGORIES
from utils.ui import apply_theme, sidebar


CATEGORY_ICONS = {
    "Food & Dining": "🍽️", "Groceries": "🛒", "Transportation": "🚗", "Fuel": "⛽",
    "Shopping": "🛍️", "Entertainment": "🎬", "Utilities": "⚡", "Internet": "🌐",
    "Mobile Bill": "📱", "Rent": "🏠", "Insurance": "🛡️", "Healthcare": "🏥",
    "Education": "🎓", "Travel": "✈️", "Clothing": "👕", "Personal Care": "✨",
    "Fitness": "💪", "Gifts & Donations": "🎁", "Savings": "💰", "Loan Payment": "🏦",
    "Emergency": "🚨", "Miscellaneous": "📌",
}


def budget_status(percent):
    if percent < 70:
        return "#22c55e", "On track"
    if percent <= 90:
        return "#f59e0b", "Watch closely"
    return "#ef4444", "Needs attention"


st.set_page_config(page_title="Budgets | FinTrack", page_icon="🎯", layout="wide")
if "logged_in" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

apply_theme()
user = st.session_state.user
sidebar(user)

st.markdown(
    """
    <style>
    .budget-page-title { margin: .2rem 0 0; color: #f8fafc; font-size: 2.15rem; letter-spacing: -.045em; }
    .budget-page-subtitle { margin: .35rem 0 1.55rem; color: #9fb0c8; font-size: 1rem; }
    .st-key-budget_entry [data-testid="stForm"] {
        margin: .25rem 0 1.7rem; padding: 1.1rem 1.15rem .7rem; border-radius: 15px;
        background: linear-gradient(145deg, rgba(31, 45, 67, .78), rgba(20, 29, 45, .74));
        border: 1px solid rgba(96, 165, 250, .20); box-shadow: 0 12px 26px rgba(1, 8, 20, .18);
    }
    .budget-section-title { color: #f1f5f9; font-size: 1.3rem; font-weight: 700; margin: 1.9rem 0 1rem; }
    .budget-section-note { color: #94a3b8; font-size: .9rem; margin: -.65rem 0 1rem; }
    .budget-card-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
    .budget-category-card {
        padding: 1.15rem; min-height: 10.7rem; border-radius: 15px;
        background: linear-gradient(145deg, rgba(34, 46, 67, .92), rgba(24, 34, 50, .87));
        border: 1px solid rgba(148, 163, 184, .20); box-shadow: 0 12px 24px rgba(1, 8, 20, .22);
        transition: transform .18s ease, border-color .18s ease;
    }
    .budget-category-card:hover { transform: translateY(-3px); border-color: rgba(96, 165, 250, .52); }
    .budget-card-heading { display: flex; align-items: center; justify-content: space-between; gap: .6rem; }
    .budget-card-heading h3 { margin: 0; color: #f8fafc; font-size: 1rem; }
    .budget-icon { font-size: 1.35rem; }
    .budget-status { font-size: .73rem; font-weight: 700; padding: .28rem .5rem; border-radius: 999px; background: rgba(148, 163, 184, .12); }
    .budget-amounts { display: flex; justify-content: space-between; gap: .7rem; margin: 1.1rem 0 .55rem; color: #cbd5e1; font-size: .83rem; }
    .budget-amounts strong { display: block; color: #f8fafc; font-size: 1rem; margin-top: .15rem; }
    .budget-amounts span:last-child { text-align: right; }
    .budget-progress-track { height: .55rem; overflow: hidden; background: rgba(15, 23, 42, .92); border-radius: 999px; }
    .budget-progress-fill { height: 100%; border-radius: inherit; }
    .budget-percent { margin-top: .5rem; color: #aebdd0; font-size: .78rem; }
    .insight-card {
        margin-top: .55rem; padding: 1.2rem 1.3rem; border-radius: 15px;
        background: linear-gradient(145deg, rgba(28, 45, 73, .8), rgba(20, 29, 45, .75));
        border: 1px solid rgba(96, 165, 250, .24); color: #cbd5e1; line-height: 1.65;
    }
    .insight-card strong { color: #f8fafc; }
    [data-testid="stPlotlyChart"] { border-radius: 15px; overflow: hidden; border: 1px solid rgba(148, 163, 184, .18); background: rgba(20, 29, 45, .45); }
    @media (max-width: 900px) { .budget-card-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (max-width: 600px) { .budget-card-grid { grid-template-columns: 1fr; } .budget-page-title { font-size: 1.8rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="budget-page-title">Budget planner</h1><p class="budget-page-subtitle">Plan monthly spending, track category usage, and stay ahead of your goals.</p>', unsafe_allow_html=True)

with st.container(key="budget_entry"):
    with st.form("budget_form", clear_on_submit=True):
        category_column, amount_column, save_column = st.columns([1.4, 1, .72])
        category = category_column.selectbox("Expense category", EXPENSE_CATEGORIES)
        amount = amount_column.number_input("Monthly budget (RM)", min_value=1.0, step=25.0, format="%.2f")
        save_budget_clicked = save_column.form_submit_button("Save budget", use_container_width=True)
        if save_budget_clicked:
            save_budget(user[0], category, amount)
            st.success(f"{category} budget saved.")
            st.rerun()

progress = get_budget_progress(user[0])
if not progress:
    st.info("No budgets created yet. Add an expense category budget above to begin monitoring your spending.")
    st.stop()

df = pd.DataFrame(progress, columns=["Category", "Budget", "Spent"])
df["Remaining"] = df["Budget"] - df["Spent"]
df["Usage"] = (df["Spent"] / df["Budget"] * 100).where(df["Budget"] > 0, 0)

total_budget = df["Budget"].sum()
total_spent = df["Spent"].sum()
remaining_budget = total_budget - total_spent
usage_percent = (total_spent / total_budget * 100) if total_budget else 0

summary_columns = st.columns(4)
summary_columns[0].metric("Total Budget", f"RM {total_budget:,.2f}")
summary_columns[1].metric("Total Spent", f"RM {total_spent:,.2f}")
summary_columns[2].metric("Remaining Budget", f"RM {remaining_budget:,.2f}")
summary_columns[3].metric("Budget Usage", f"{usage_percent:.1f}%")

chart_column, insights_column = st.columns([1.15, .85], gap="large")
with chart_column:
    st.markdown('<h2 class="budget-section-title">Budget allocation</h2><p class="budget-section-note">How your monthly budget is distributed across categories.</p>', unsafe_allow_html=True)
    allocation_chart = px.pie(df, names="Category", values="Budget", hole=.62, color_discrete_sequence=px.colors.sequential.Blues_r)
    allocation_chart.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#cbd5e1"},
        margin={"l": 14, "r": 14, "t": 22, "b": 22},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.22, "xanchor": "center", "x": .5},
    )
    allocation_chart.update_traces(textinfo="percent", textfont={"color": "#f8fafc"}, hovertemplate="<b>%{label}</b><br>Budget: RM %{value:,.2f}<extra></extra>")
    st.plotly_chart(allocation_chart, width="stretch", config={"displayModeBar": False})

with insights_column:
    st.markdown('<h2 class="budget-section-title">Budget insights</h2><p class="budget-section-note">Live guidance based on this month’s spending.</p>', unsafe_allow_html=True)
    highest = df.loc[df["Usage"].idxmax()]
    over_budget = df[df["Usage"] > 100]
    near_limit = df[(df["Usage"] >= 90) & (df["Usage"] <= 100)]
    if not over_budget.empty:
        category_label = "category is" if len(over_budget) == 1 else "categories are"
        message = f"<strong>Action needed:</strong> {len(over_budget)} {category_label} over budget. Review {html.escape(str(over_budget.iloc[0]['Category']))} first."
    elif not near_limit.empty:
        category_label = "category is" if len(near_limit) == 1 else "categories are"
        message = f"<strong>Almost at the limit:</strong> {len(near_limit)} {category_label} at 90% or more. {html.escape(str(near_limit.iloc[0]['Category']))} needs close attention."
    elif total_spent == 0:
        message = "<strong>Ready to track:</strong> Your budgets are set, but there is no spending recorded for this month yet."
    else:
        message = f"<strong>You’re on track:</strong> Overall usage is {usage_percent:.1f}%. Your highest usage is {html.escape(str(highest['Category']))} at {highest['Usage']:.1f}%."
    st.markdown(f'<div class="insight-card">{message}<br><br><strong>Remaining:</strong> RM {remaining_budget:,.2f} is available across all active budgets.</div>', unsafe_allow_html=True)

st.markdown('<h2 class="budget-section-title">Category progress</h2><p class="budget-section-note">Green is under 70%, orange is 70–90%, and red means a category needs attention.</p>', unsafe_allow_html=True)

cards = []
for row in df.sort_values("Usage", ascending=False).itertuples(index=False):
    color, status = budget_status(row.Usage)
    icon = CATEGORY_ICONS.get(row.Category, "📌")
    width = max(0, min(float(row.Usage), 100))
    cards.append(
        f'''<article class="budget-category-card">
            <div class="budget-card-heading"><h3><span class="budget-icon">{icon}</span> {html.escape(str(row.Category))}</h3><span class="budget-status" style="color:{color}">{status}</span></div>
            <div class="budget-amounts"><span>Spent<strong>RM {row.Spent:,.2f}</strong></span><span>Budget<strong>RM {row.Budget:,.2f}</strong></span></div>
            <div class="budget-progress-track"><div class="budget-progress-fill" style="width:{width:.2f}%; background:{color}"></div></div>
            <div class="budget-percent">{row.Usage:.1f}% used · RM {row.Remaining:,.2f} remaining</div>
        </article>'''
    )
st.markdown(f'<section class="budget-card-grid">{"".join(cards)}</section>', unsafe_allow_html=True)
