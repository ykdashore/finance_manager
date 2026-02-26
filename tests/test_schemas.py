"""Tests for Pydantic schemas validation."""
import pytest
from pydantic import ValidationError

from app.models.schemas import ChatSchema, ChatResponseSchema


class TestChatSchema:
    """Test ChatSchema validation."""

    def test_valid_chat_message(self):
        """Test creating valid chat schema."""
        data = {
            "message": "I spent 500 on groceries",
            "user_id": "user123",
            "thread_id": "thread456",
            "tz": "Asia/Kolkata"
        }
        schema = ChatSchema(**data)
        assert schema.message == "I spent 500 on groceries"
        assert schema.user_id == "user123"

    def test_missing_required_fields(self):
        """Test that required fields are mandatory."""
        with pytest.raises(ValidationError):
            ChatSchema(message="test", user_id="user123")

    def test_timezone_optional(self):
        """Test that timezone is optional."""
        data = {
            "message": "test",
            "user_id": "user123",
            "thread_id": "thread456"
        }
        schema = ChatSchema(**data)
        assert schema.tz is None


class TestChatResponseSchema:
    """Test ChatResponseSchema validation."""

    def test_valid_response(self):
        """Test creating valid response schema."""
        data = {
            "user_id": "user123",
            "thread_id": "thread456",
            "user_message": "I spent money",
            "agent_response": "Logged: ₹500 on groceries"
        }
        schema = ChatResponseSchema(**data)
        assert schema.status == "success"  # Default
        assert schema.user_id == "user123"

    def test_invalid_agent_response_type(self):
        """Test that agent_response must be string."""
        data = {
            "user_id": "user123",
            "thread_id": "thread456",
            "user_message": "test",
            "agent_response": {"invalid": "dict"}
        }
        with pytest.raises(ValidationError):
            ChatResponseSchema(**data)
