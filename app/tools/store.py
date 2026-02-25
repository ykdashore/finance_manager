import sqlite3
import datetime
from typing import Dict, Any
from langchain_core.tools import tool
from app.core.config import DB_PATH
from app.models.entities import Expense
from app.db.session import SessionLocal


def init_db():
    """Initialize the database with schema."""
    try:
        import os
        
        # Ensure database directory exists
        db_dir = os.path.dirname(DB_PATH) or "."
        os.makedirs(db_dir, exist_ok=True)
        
        schema_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "db", 
            "schema.sql"
        )
        
        with sqlite3.connect(DB_PATH) as conn:
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
                conn.commit()
    except Exception as e:
        print(f"Warning: Database initialization issue: {e}")



@tool
def log_expense(user_id: str, entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stores an expense row into the database using SQLAlchemy ORM.
    Required entry fields: ts, amount, category, currency, description, merchant, raw_text
    """
    db = SessionLocal()
    try:
        expense = Expense(
        user_id=user_id,
        ts=entry["ts"],
        amount=float(entry["amount"]),
        currency=entry.get("currency", "INR"),
        category=entry["category"],
        description=entry.get("description"),
        merchant=entry.get("merchant"),
        raw_text=entry.get("raw_text"),
        created_at=entry.get("created_at", datetime.datetime.now())
    )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return {"expense_id": expense.id}
    finally:
        db.close()