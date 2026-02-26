"""Tests for chat API endpoints."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from langchain_core.messages import AIMessage


class TestChatAPI:
    """Test chat endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client with chat router."""
        from app.api.chat import router
        
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    def test_send_message_success(self, client, sample_chat_request):
        """Test sending a message successfully."""
        with patch("app.api.chat.get_graph") as mock_get_graph:
            mock_graph = MagicMock()
            mock_get_graph.return_value = mock_graph
            
            # Mock the response - graph.invoke returns dict with "messages" key
            mock_message = AIMessage(content="Logged: ₹500 on groceries")
            mock_graph.invoke.return_value = {"messages": [mock_message]}
            
            response = client.post("/api/chat/message", json=sample_chat_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["user_id"] == "test_user"

    def test_missing_required_fields(self, client):
        """Test that required fields are validated."""
        incomplete_request = {
            "message": "I spent money"
        }
        
        response = client.post("/api/chat/message", json=incomplete_request)
        assert response.status_code == 422  # Validation error

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/chat/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
