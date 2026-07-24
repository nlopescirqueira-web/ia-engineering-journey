import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.environ.get("AGENT_DB_PATH", "data/agent.db")


def _connect() -> sqlite3.Connection:
    dirname = os.path.dirname(DB_PATH)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                input_text TEXT NOT NULL,
                action TEXT NOT NULL,
                title TEXT,
                due_date TEXT,
                notes TEXT,
                reply TEXT
            )
            """
        )


def log_interaction(
    input_text: str,
    action: str,
    title: str | None = None,
    due_date: str | None = None,
    notes: str | None = None,
    reply: str | None = None,
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO interactions
                (created_at, input_text, action, title, due_date, notes, reply)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                input_text,
                action,
                title,
                due_date,
                notes,
                reply,
            ),
        )
