import sqlite3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any

import pandas as pd
from langchain_core.tools import tool

from app.core.config import DB_PATH


def _week_bounds(now_local: datetime):
    start = (now_local - timedelta(days=now_local.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end = start + timedelta(days=7)
    return start, end


@tool
def weekly_report(user_id: str, tz: str = "Asia/Kolkata") -> Dict[str, Any]:
    """
    Compute weekly totals, category split, daily totals and a few insights.
    """
    now_local = datetime.now(ZoneInfo(tz))
    start, end = _week_bounds(now_local)

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """SELECT ts, amount, currency, category, description, merchant
            FROM expenses
            WHERE user_id = ? AND ts >= ? AND ts < ?
            """,
            conn,
            params=(user_id, start.isoformat(), end.isoformat()),
        )

    if df.empty:
        return {
            "week_start": start.date().isoformat(),
            "week_end": (end.date() - timedelta(days=1)).isoformat(),
            "total": 0.0,
            "by_category": {},
            "by_day": {},
            "top_items": [],
            "insights": ["No expenses logged this week yet."],
        }

    df["ts"] = pd.to_datetime(df["ts"])
    df["day"] = df["ts"].dt.date.astype(str)

    total = float(df["amount"].sum())
    by_category = (
        df.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict()
    )
    by_day = df.groupby("day")["amount"].sum().sort_index().to_dict()

    top = df.sort_values("amount", ascending=False).head(5)

    top_items = [
        {
            "amount": float(r.amount),
            "category": r.category,
            "description": r.description,
            "merchant": r.merchant,
            "day": str(r.day),
        }
        for r in top.itertuples()
    ]

    biggest_cat, biggest_val = max(by_category.items(), key=lambda x: x[1])
    insights = [
        f"Highest spend category: {biggest_cat} (amount {biggest_val})",
        f"Avg per active day: {total / max(len(by_day), 1):.0f}",
    ]

    return {
        "week_start": start.date().isoformat(),
        "week_end": (end.date() - timedelta(days=1)).isoformat(),
        "total": total,
        "by_category": by_category,
        "by_day": by_day,
        "top_items": top_items,
        "insights": insights,
    }
