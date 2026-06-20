import sqlite3
import json
import uuid
from datetime import datetime

DB_PATH = "aria.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS research_history (
            id TEXT PRIMARY KEY,
            query TEXT NOT NULL,
            report TEXT NOT NULL,
            sources TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_research(query: str, report: str, sources: list) -> str:
    conn = sqlite3.connect(DB_PATH)
    research_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO research_history (id, query, report, sources, created_at) VALUES (?, ?, ?, ?, ?)",
        (research_id, query, report, json.dumps(sources), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return research_id

def get_history(limit: int = 30) -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, query, created_at FROM research_history ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_research_by_id(research_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM research_history WHERE id = ?", (research_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    result = dict(row)
    result["sources"] = json.loads(result["sources"]) if result["sources"] else []
    return result