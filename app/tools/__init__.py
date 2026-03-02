from app.tools.processor import process_expense
from app.tools.store import log_expense, update_expense, delete_expense, find_expenses
from app.tools.analytics import weekly_report

# Merged tool that handles extraction + categorization
ALL_TOOLS = [
    process_expense,
    log_expense,
    update_expense,
    delete_expense,
    find_expenses,
    weekly_report,
]
