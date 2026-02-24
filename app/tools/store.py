import sqlite3
import datetime
from typing import Dict, Any
from langchain_core.tools import tool
from app.config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
         with open("app/db/schema.sql", "r", encoding="utf-8") as f:
              conn. executescript(f.read())


@tool              
def log_expense(user_id: str, entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stores an expense row into the SQLite database.
    Required entry fields: ts, amount, category, currency, description, merchant, raw_text
    """
    now = datetime.datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO expenses (
                user_id, ts, amount, currency, category, 
                description, merchant, raw_text, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                entry["ts"],
                float(entry["amount"]),
                entry.get("currency", "INR"),
                entry["category"],
                entry.get("description"),
                entry.get("merchant"),
                entry.get("raw_text"),
                now
            )
        )
        conn.commit()
        
    return {"expense_id": cur.lastrowid}