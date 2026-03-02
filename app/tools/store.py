import sqlite3
import datetime
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from app.core.config import DB_PATH
from app.models.entities import Expense
from app.db.session import SessionLocal
from sqlalchemy import func


def init_db():
    """Initialize the database with schema."""
    try:
        import os

        db_dir = os.path.dirname(DB_PATH) or "."
        os.makedirs(db_dir, exist_ok=True)

        schema_path = os.path.join(os.path.dirname(__file__), "..", "db", "schema.sql")

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
            created_at=entry.get("created_at", datetime.datetime.now()),
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return {"expense_id": expense.id}
    finally:
        db.close()


@tool
def update_expense(expense_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update fields of an existing expense.
    Allowed fields: amount, category, description, merchant, ts
    """
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            return {"error": "Expense not found"}

        for key, value in updates.items():
            if hasattr(expense, key):
                setattr(expense, key, value)

        db.commit()
        db.refresh(expense)
        return {"updated_expense_id": expense.id}
    finally:
        db.close()


@tool
def delete_expense(expense_id: int) -> Dict[str, Any]:
    """
    Delete an expense by ID.
    """
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            return {"error": "Expense not found"}

        db.delete(expense)
        db.commit()
        return {"deleted_expense_id": expense_id}
    finally:
        db.close()


@tool
def find_expenses(
    user_id: str,
    description: Optional[str] = None,
    merchant: Optional[str] = None,
    date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Find expenses matching given filters.
    Used for resolving update/delete intent.
    """
    db = SessionLocal()
    try:
        query = db.query(Expense).filter(Expense.user_id == user_id)

        if description:
            query = query.filter(Expense.description.ilike(f"%{description}%"))

        if merchant:
            query = query.filter(Expense.merchant.ilike(f"%{merchant}%"))

        if date:
            query = query.filter(func.date(Expense.created_at) == date)

        results = query.order_by(Expense.created_at.desc()).limit(5).all()

        return [
            {
                "id": e.id,
                "amount": e.amount,
                "category": e.category,
                "description": e.description,
                "merchant": e.merchant,
                "created_at": e.created_at.isoformat(),
            }
            for e in results
        ]
    finally:
        db.close()
