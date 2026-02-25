from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import WeeklyReportResponseSchema
from app.tools.analytics import weekly_report
from app.core.config import APP_TZ

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/weekly-report", response_model=WeeklyReportResponseSchema)
def get_weekly_report(
    user_id: str = Query(..., description="User ID"),
    tz: str = Query(APP_TZ, description="Timezone (e.g., Asia/Kolkata)")
):
    """
    Generate a weekly expense report for the user.
    
    Returns:
    - Total spending for the week
    - Breakdown by category
    - Daily totals
    - Top 5 expenses
    - Insights and patterns
    """
    try:
        report = weekly_report(user_id, tz)
        return WeeklyReportResponseSchema(**report)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating weekly report: {str(e)}"
        )


@router.get("/health")
def health_check():
    """Health check endpoint for analytics service."""
    return {"status": "healthy", "service": "finance-manager-analytics"}
