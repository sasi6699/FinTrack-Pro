import sqlite3
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.categories import ALL_CATEGORIES

DB_PATH = os.path.join(os.path.dirname(__file__), "finance.db")


def create_database():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON")

    cursor = conn.cursor()

    # ==========================
    # USERS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ==========================
    # TRANSACTIONS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transaction_date TEXT NOT NULL,
        description TEXT,
        category TEXT,
        transaction_type TEXT CHECK(transaction_type IN ('Income','Expense')),
        amount REAL NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # ==========================
    # CATEGORIES
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    )
    """)

    # ==========================
    # BUDGETS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets(
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        monthly_limit REAL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # ==========================
    # IMPORT LOGS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS import_logs(
        import_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        imported_date TEXT,
        records INTEGER
    )
    """)

    # Keep legacy rows intact while seeding all current category values.
    for category in ALL_CATEGORIES:
        cursor.execute("""
            INSERT OR IGNORE INTO categories(category_name)
            VALUES(?)
        """, (category,))

    conn.commit()
    conn.close()

    print("=" * 50)
    print("FinTrack Pro Database Created Successfully")
    print("=" * 50)


if __name__ == "__main__":
    create_database()
