import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.chat import router as chat_router
from app.api.analytics import router as analytics_router
from app.core import config

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage app lifecycle - startup and shutdown events.
    """
    logger.info("Finance Manager API starting up...")
    try:
        # Initialize database on startup
        from app.tools.store import init_db

        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    yield

    logger.info("Finance Manager API shutting down...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Finance Manager API",
    description="AI-powered personal finance manager using LangGraph and Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(chat_router)
app.include_router(analytics_router)


# Root endpoint
@app.get("/", tags=["health"])
def root():
    """Root endpoint - API status"""
    return {
        "service": "Finance Manager API",
        "version": "1.0.0",
        "status": "running",
        "docs_url": "/docs",
        "endpoints": {
            "chat": "/api/chat/message",
            "weekly_report": "/api/analytics/weekly-report",
            "health": "/docs",
        },
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Finance Manager API server...")
    uvicorn.run("main:app", host="localhost", port=8002, reload=True, log_level="info")
