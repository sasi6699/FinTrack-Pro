import sqlite3

DATABASE = "database/finance.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def save_budget(user_id, category, monthly_limit):
    with get_connection() as conn:
        existing = conn.execute("SELECT budget_id FROM budgets WHERE user_id=? AND category=?", (user_id, category)).fetchone()
        if existing:
            conn.execute("UPDATE budgets SET monthly_limit=? WHERE budget_id=?", (monthly_limit, existing[0]))
        else:
            conn.execute("INSERT INTO budgets(user_id, category, monthly_limit) VALUES (?, ?, ?)", (user_id, category, monthly_limit))


def get_budgets(user_id):
    with get_connection() as conn:
        return conn.execute("SELECT category, monthly_limit FROM budgets WHERE user_id=? ORDER BY category", (user_id,)).fetchall()


def get_budget_progress(user_id, month_prefix=None):
    month_prefix = month_prefix or __import__('datetime').date.today().strftime('%Y-%m')
    with get_connection() as conn:
        return conn.execute("""SELECT b.category, b.monthly_limit,
            COALESCE(SUM(t.amount), 0) AS spent FROM budgets b
            LEFT JOIN transactions t ON t.user_id=b.user_id AND t.category=b.category
              AND t.transaction_type='Expense' AND t.transaction_date LIKE ?
            WHERE b.user_id=? GROUP BY b.budget_id, b.category, b.monthly_limit
            ORDER BY spent DESC""", (f'{month_prefix}%', user_id)).fetchall()
