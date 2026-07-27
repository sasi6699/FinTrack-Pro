import streamlit as st
import pandas as pd
from datetime import date
from utils.transaction import add_transaction, get_transactions, get_transaction, update_transaction, delete_transaction
from utils.ui import apply_theme, sidebar
from utils.categories import categories_for

st.set_page_config(page_title="Transactions | FinTrack", page_icon="💳", layout="wide")
if "user" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()
apply_theme()
user_id = st.session_state.user[0]
sidebar(st.session_state.user)

st.title("Transaction management")
st.caption("Add, search, edit, and remove financial records.")
add_tab, manage_tab = st.tabs(["Add transaction", "Search & manage"])

with add_tab:
    kind = st.selectbox("Type", ["Expense", "Income"], key="add_transaction_type")
    with st.form("add_transaction", clear_on_submit=True):
        left, right = st.columns(2)
        with left:
            category = st.selectbox("Category", categories_for(kind), key=f"add_category_{kind}")
            amount = st.number_input("Amount (RM)", min_value=0.01, format="%.2f")
        with right:
            tx_date = st.date_input("Date", value=date.today())
            description = st.text_area("Description", placeholder="e.g. Weekly grocery shop")
        if st.form_submit_button("Save transaction", use_container_width=True):
            add_transaction(user_id, kind, category, description, amount, str(tx_date))
            st.success("Transaction saved.")

with manage_tab:
    rows = get_transactions(user_id)
    if not rows:
        st.info("No transactions yet. Add one to start tracking your money.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Date", "Type", "Category", "Description", "Amount (RM)"])
        query = st.text_input("Search transactions", placeholder="Search date, category, description, type, or amount")
        type_filter = st.multiselect("Filter by type", ["Income", "Expense"], default=["Income", "Expense"])
        filtered = df[df["Type"].isin(type_filter)]
        if query:
            filtered = filtered[filtered.astype(str).apply(lambda r: r.str.contains(query, case=False, na=False).any(), axis=1)]
        st.caption(f"Showing {len(filtered)} of {len(df)} transactions")
        st.dataframe(filtered, hide_index=True, use_container_width=True)
        choices = filtered["ID"].tolist()
        if choices:
            selected_id = st.selectbox("Select a transaction to edit or delete", choices, format_func=lambda x: f"#{x} · {df.loc[df.ID == x, 'Description'].iloc[0] or 'No description'}")
            record = get_transaction(user_id, selected_id)
            with st.expander("Edit selected transaction", expanded=True):
                edit_type = st.selectbox(
                    "Type",
                    ["Income", "Expense"],
                    index=["Income", "Expense"].index(record[2]),
                    key=f"edit_type_{selected_id}",
                )
                legacy_category = record[3] if edit_type == record[2] else None
                edit_categories = categories_for(edit_type, legacy_category)
                with st.form("edit_transaction"):
                    a, b = st.columns(2)
                    with a:
                        edit_category = st.selectbox(
                            "Category",
                            edit_categories,
                            index=edit_categories.index(record[3]) if record[3] in edit_categories else 0,
                            key=f"edit_category_{selected_id}_{edit_type}",
                        )
                        edit_amount = st.number_input("Amount (RM)", min_value=0.01, value=float(record[5]), format="%.2f", key="edit_amount")
                    with b:
                        edit_date = st.date_input("Date", value=pd.to_datetime(record[1]).date(), key="edit_date")
                        edit_description = st.text_area("Description", value=record[4] or "", key="edit_description")
                    if st.form_submit_button("Update transaction"):
                        update_transaction(user_id, selected_id, edit_type, edit_category, edit_description, edit_amount, str(edit_date))
                        st.success("Transaction updated.")
                        st.rerun()
                if st.button("Delete selected transaction", type="secondary"):
                    delete_transaction(user_id, selected_id)
                    st.success("Transaction deleted.")
                    st.rerun()
