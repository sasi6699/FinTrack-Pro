import sqlite3
from datetime import datetime

DATABASE = "database/finance.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def add_transaction(user_id, transaction_type, category, description, amount, transaction_date=None):
    transaction_date = transaction_date or datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute("""INSERT INTO transactions
            (user_id, transaction_date, description, category, transaction_type, amount)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, transaction_date, description, category, transaction_type, amount))


def get_transactions(user_id):
    with get_connection() as conn:
        return conn.execute("""SELECT transaction_id, transaction_date, transaction_type,
            category, description, amount FROM transactions WHERE user_id=?
            ORDER BY transaction_date DESC, transaction_id DESC""", (user_id,)).fetchall()


def get_transaction(user_id, transaction_id):
    with get_connection() as conn:
        return conn.execute("""SELECT transaction_id, transaction_date, transaction_type,
            category, description, amount FROM transactions
            WHERE user_id=? AND transaction_id=?""", (user_id, transaction_id)).fetchone()


def delete_transaction(user_id, transaction_id):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM transactions WHERE transaction_id=? AND user_id=?", (transaction_id, user_id))
        return cursor.rowcount > 0


def update_transaction(user_id, transaction_id, transaction_type, category, description, amount, transaction_date):
    with get_connection() as conn:
        cursor = conn.execute("""UPDATE transactions SET transaction_date=?, transaction_type=?,
            category=?, description=?, amount=? WHERE transaction_id=? AND user_id=?""",
            (transaction_date, transaction_type, category, description, amount, transaction_id, user_id))
        return cursor.rowcount > 0


def get_dashboard_summary(user_id):
    with get_connection() as conn:
        income = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id=? AND transaction_type='Income'", (user_id,)).fetchone()[0]
        expense = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id=? AND transaction_type='Expense'", (user_id,)).fetchone()[0]
        count = conn.execute("SELECT COUNT(*) FROM transactions WHERE user_id=?", (user_id,)).fetchone()[0]
    return {"income": income, "expense": expense, "balance": income - expense, "transactions": count}
