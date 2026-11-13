import os
import sqlite3
import hashlib
import secrets

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users.db")


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_users():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)


def make_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"),
        salt.encode("utf-8"), 200000
    ).hex()


def create_user(name, email, password):
    salt = secrets.token_hex(16)
    password_hash = make_password(password, salt)
    try:
        with connect() as db:
            cursor = db.execute(
                "INSERT INTO users (name, email, password_hash, salt) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, salt)
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email):
    with connect() as db:
        return db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()


def get_user_by_id(user_id):
    with connect() as db:
        return db.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()


def check_user_password(user, password):
    if not user:
        return False
    password_hash = make_password(password, user["salt"])
    return secrets.compare_digest(password_hash, user["password_hash"])
