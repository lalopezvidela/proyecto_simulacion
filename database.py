import os
import sqlite3
from pathlib import Path

import bcrypt


def get_default_db_path() -> str:
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)
    return str(data_dir / "usuarios.db")


def create_tables(db_path: str | None = None) -> str:
    db_path = db_path or get_default_db_path()
    directory = os.path.dirname(db_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    return db_path


def register_user(full_name: str, username: str, email: str, password: str, db_path: str | None = None) -> bool:
    if not full_name.strip() or not username.strip() or not password:
        return False

    db_path = create_tables(db_path)
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        existing = conn.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username.strip(),),
        ).fetchone()
        if existing:
            return False

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn.execute(
            "INSERT INTO users (full_name, username, email, password_hash) VALUES (?, ?, ?, ?)",
            (full_name.strip(), username.strip(), email.strip(), password_hash),
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        if conn is not None:
            conn.close()


def authenticate_user(username: str, password: str, db_path: str | None = None) -> bool:
    db_path = db_path or get_default_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username.strip(),),
        ).fetchone()
        if not row:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), row[0].encode("utf-8"))
    except (sqlite3.Error, ValueError):
        return False
    finally:
        if conn is not None:
            conn.close()
