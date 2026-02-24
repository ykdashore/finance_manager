from app.tools.processor import process_expense
from app.tools.store import log_expense, init_db
from app.tools.analytics import weekly_report

# Merged tool that handles extraction + categorization
ALL_TOOLS = [process_expense, log_expense, weekly_report]

