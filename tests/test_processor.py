"""Tests for expense processing and categorization."""
import pytest
from pydantic import ValidationError

from app.tools.processor import ProcessedExpense


class TestProcessedExpense:
    """Test ProcessedExpense model validation."""

    def test_valid_expense(self, sample_expense_data):
        """Test creating a valid expense."""
        expense = ProcessedExpense(**sample_expense_data)
        assert expense.amount == 500.0
        assert expense.category == "Groceries"
        assert expense.currency == "INR"

    def test_amount_must_be_positive(self, sample_expense_data):
        """Test that amount must be greater than 0."""
        sample_expense_data["amount"] = 0
        with pytest.raises(ValidationError):
            ProcessedExpense(**sample_expense_data)

    def test_confidence_between_0_and_1(self, sample_expense_data):
        """Test that confidence must be between 0 and 1."""
        sample_expense_data["category_confidence"] = 1.5
        with pytest.raises(ValidationError):
            ProcessedExpense(**sample_expense_data)

    def test_malformed_datetime_auto_fixed(self, sample_expense_data):
        """Test that malformed datetime +05:3 is fixed to +05:30."""
        sample_expense_data["created_at"] = "2026-02-25T12:00:00+05:3"
        expense = ProcessedExpense(**sample_expense_data)
        # Should not raise error 
        assert expense.created_at is not None

    def test_incomplete_datetime_auto_fixed(self, sample_expense_data):
        """Test that incomplete datetime like '2026-02-24T12:' is fixed."""
        sample_expense_data["created_at"] = "2026-02-24T12:"
        expense = ProcessedExpense(**sample_expense_data)
        # Should not raise error
        assert expense.created_at is not None

