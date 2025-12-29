import sqlite3
from datetime import datetime

DB_PATH = "sessions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_session(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions VALUES (?, ?)",
        (session_id, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def session_exists(session_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM sessions WHERE session_id = ?",
        (session_id,)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
