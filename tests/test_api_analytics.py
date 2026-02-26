"""Tests for analytics API endpoints."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.core.config import APP_TZ


class TestAnalyticsAPI:
    """Test analytics endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client with analytics router."""
        from app.api.analytics import router
        
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    def test_weekly_report_success(self, client):
        """Test getting weekly report."""
        mock_report = {
            "week_start": "2026-02-23",
            "week_end": "2026-03-01",
            "total": 2500.0,
            "by_category": {"Groceries": 1500.0},
            "by_day": {"2026-02-25": 500.0},
            "top_items": [],
            "insights": ["High spending"]
        }
        
        with patch("app.api.analytics.weekly_report") as mock_weekly:
            # Make it callable and return the dict directly
            mock_weekly.side_effect = lambda user_id, tz: mock_report
            
            response = client.get("/api/analytics/weekly-report?user_id=test_user")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2500.0

    def test_missing_user_id(self, client):
        """Test that user_id is required."""
        response = client.get("/api/analytics/weekly-report")
        assert response.status_code == 422

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/analytics/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
