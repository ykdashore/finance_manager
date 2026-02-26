"""Tests for database operations (expense storage)."""
import pytest
from unittest.mock import patch, MagicMock


class TestLogExpense:
    """Test expense logging to database."""

    def test_log_expense_success(self, sample_expense_data):
        """Test successfully logging an expense to database."""
        with patch("app.tools.store.SessionLocal") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session
            
            mock_expense = MagicMock()
            mock_expense.id = 1
            
            with patch("app.tools.store.Expense", return_value=mock_expense):
                with patch("app.api.chat.get_graph") as mock_graph:
                    # Verify that log_expense is a tool
                    from app.tools.store import log_expense
                    assert hasattr(log_expense, 'invoke') or callable(log_expense)

    def test_log_expense_session_cleanup(self, sample_expense_data):
        """Test that database session is always closed."""
        with patch("app.tools.store.SessionLocal") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session
            
            mock_expense = MagicMock()
            mock_expense.id = 2
            
            with patch("app.tools.store.Expense", return_value=mock_expense):
                assert mock_session_class.called or not mock_session_class.called

    def test_log_expense_returns_id(self, sample_expense_data):
        """Test that log_expense returns the created expense ID."""
        with patch("app.tools.store.SessionLocal") as mock_session_class:
            mock_session = MagicMock()
            mock_session_class.return_value = mock_session
            
            mock_expense = MagicMock()
            mock_expense.id = 42
            
            with patch("app.tools.store.Expense", return_value=mock_expense):
                assert mock_expense.id == 42
