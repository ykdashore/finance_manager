import pytest


@pytest.fixture
def sample_expense_data():
    """Sample expense data for testing."""
    return {
        "amount": 500.0,
        "ts": "2026-02-25T12:00:00+05:30",
        "description": "groceries",
        "category": "Groceries",
        "category_confidence": 0.95,
        "created_at": "2026-02-25T12:00:00+05:30",
        "currency": "INR",
        "merchant": None,
        "notes": None,
        "is_ambiguous": False,
        "clarification_question": None,
    }


@pytest.fixture
def sample_chat_request():
    """Sample chat request data."""
    return {
        "message": "I spent 500 on groceries yesterday",
        "user_id": "test_user",
        "thread_id": "test_thread",
        "tz": "Asia/Kolkata",
    }
