from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime

# Request Schemas
class ChatSchema(BaseModel):
    """Chat message request from user"""
    message: str = Field(..., description="User's message to the finance manager")
    user_id: str = Field(..., description="Unique user identifier")
    thread_id: str = Field(..., description="Thread/conversation ID")
    tz: Optional[str] = Field(None, description="User's timezone (e.g., Asia/Kolkata)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I spent 500 on groceries yesterday",
                "user_id": "user123",
                "thread_id": "thread456",
                "tz": "Asia/Kolkata"
            }
        }


# Response Schemas
class ChatResponseSchema(BaseModel):
    """Chat message response from agent"""
    user_id: str
    thread_id: str
    user_message: str
    agent_response: str
    status: str = "success"
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "thread_id": "thread456",
                "user_message": "I spent 500 on groceries",
                "agent_response": "Logged: ₹500 spent on groceries in Groceries category",
                "status": "success",
                "timestamp": "2026-02-25T10:30:00"
            }
        }


class ExpenseItemSchema(BaseModel):
    """Individual expense item in report"""
    amount: float = Field(..., description="Expense amount")
    category: str = Field(..., description="Expense category")
    description: str = Field(..., description="Short description")
    merchant: Optional[str] = Field(None, description="Merchant name if available")
    day: str = Field(..., description="Date of expense (YYYY-MM-DD)")


class WeeklyReportResponseSchema(BaseModel):
    """Weekly expense report response"""
    week_start: str = Field(..., description="Start date of the week (YYYY-MM-DD)")
    week_end: str = Field(..., description="End date of the week (YYYY-MM-DD)")
    total: float = Field(..., description="Total spending for the week")
    by_category: Dict[str, float] = Field(..., description="Spending breakdown by category")
    by_day: Dict[str, float] = Field(..., description="Daily spending totals")
    top_items: List[ExpenseItemSchema] = Field(..., description="Top 5 expenses")
    insights: List[str] = Field(..., description="Generated insights and patterns")

    class Config:
        json_schema_extra = {
            "example": {
                "week_start": "2026-02-23",
                "week_end": "2026-03-01",
                "total": 3500.0,
                "by_category": {
                    "Groceries": 1500.0,
                    "Food & Dining": 1200.0,
                    "Transport": 800.0
                },
                "by_day": {
                    "2026-02-23": 500.0,
                    "2026-02-24": 800.0
                },
                "top_items": [
                    {
                        "amount": 800.0,
                        "category": "Food & Dining",
                        "description": "dinner",
                        "merchant": "Restaurant ABC",
                        "day": "2026-02-24"
                    }
                ],
                "insights": [
                    "Highest spend category: Food & Dining (₹1200)",
                    "Avg per active day: ₹875"
                ]
            }
        }


class HealthCheckSchema(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)