import sqlite3
import hashlib

# SQLite database location
DB_PATH = "database/finance.db"


def get_connection():
    """
    Create and return a database connection.
    """
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    """
    Convert a plain-text password into a SHA-256 hash.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(full_name, email, password):
    """
    Register a new user.
    Returns:
        (True, message) on success
        (False, message) on failure
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False, "Email already exists."

    # Encrypt password
    encrypted_password = hash_password(password)

    # Save user
    cursor.execute("""
        INSERT INTO users (full_name, email, password)
        VALUES (?, ?, ?)
    """, (
        full_name,
        email,
        encrypted_password
    ))

    conn.commit()
    conn.close()

    return True, "Registration successful!"


def login_user(email, password):
    """
    Login validation.
    Returns:
        (True, user information)
        (False, error message)
    """

    conn = get_connection()
    cursor = conn.cursor()

    encrypted_password = hash_password(password)

    cursor.execute("""
        SELECT user_id, full_name, email
        FROM users
        WHERE email = ? AND password = ?
    """, (
        email,
        encrypted_password
    ))

    user = cursor.fetchone()

    conn.close()

    if user:
        return True, user

    return False, "Invalid email or password."