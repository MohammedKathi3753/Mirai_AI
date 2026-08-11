import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_NAME = "mirai_ai.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """Create the users table if it does not already exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            education TEXT NOT NULL,
            job_role TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    full_name,
    email,
    education,
    job_role,
    password
):
    """
    Create a new user account.

    The password is hashed before being stored in the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Securely hash the password
    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""
            INSERT INTO users (
                full_name,
                email,
                education,
                job_role,
                password
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            education,
            job_role,
            hashed_password
        ))

        connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."

    finally:

        connection.close()


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(email, password):
    """Check whether the provided email and password are correct."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            email,
            education,
            job_role,
            password
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    stored_password = user[5]

    if check_password_hash(
        stored_password,
        password
    ):
        return user

    return None