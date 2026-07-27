import streamlit as st
import pandas as pd

from utils.transaction import get_transactions

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

user = st.session_state.user
user_id = user[0]

st.title("📄 Financial Reports")
st.divider()

transactions = get_transactions(user_id)

if len(transactions) == 0:
    st.info("No transaction data available.")
    st.stop()

df = pd.DataFrame(
    transactions,
    columns=[
        "ID",
        "Date",
        "Type",
        "Category",
        "Description",
        "Amount"
    ]
)

st.subheader("📋 Transaction Report")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()
st.subheader("📥 Export Reports")

col1, col2 = st.columns(2)

# ===============================
# CSV Export
# ===============================

with col1:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name="transactions.csv",
        mime="text/csv",
        use_container_width=True
    )

# ===============================
# Excel Export
# ===============================

with col2:

    from io import BytesIO

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Transactions"
        )

    excel_data = output.getvalue()

    st.download_button(
        label="📊 Download Excel",
        data=excel_data,
        file_name="transactions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()
from io import BytesIO
from reportlab.pdfgen import canvas

st.subheader("📑 PDF Summary")

pdf_buffer = BytesIO()

pdf = canvas.Canvas(pdf_buffer)

pdf.setFont("Helvetica-Bold", 16)
pdf.drawString(50, 800, "FinTrack Pro Report")

pdf.setFont("Helvetica", 12)
pdf.drawString(50, 770, f"Total Transactions: {len(df)}")

income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

pdf.drawString(50, 740, f"Total Income : RM {income:.2f}")
pdf.drawString(50, 720, f"Total Expense: RM {expense:.2f}")
pdf.drawString(50, 700, f"Balance      : RM {balance:.2f}")

pdf.save()

pdf_buffer.seek(0)

st.download_button(
    label="📑 Download PDF Report",
    data=pdf_buffer,
    file_name="Financial_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)