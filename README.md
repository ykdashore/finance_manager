# Finance Manager
## Overview

Finance Manager is an AI-powered expense tracking agent built with LangGraph and Google Gemini that intelligently processes natural language messages to extract, categorize, and log personal expenses. It provides automated weekly expense analysis with category breakdowns.

## Features

### 1. **Chat Endpoint** (`/api/chat/message`)
- Send natural language messages to the finance manager
- Automatically extracts expenses from text
- Categorizes expenses (Groceries, Food & Dining, Transport, etc.)
- Stores expenses in the database
- Maintains conversation history per thread

### 2. **Analytics Endpoint** (`/api/analytics/weekly-report`)
- Generates weekly expense summaries
- Breakdown by category
- Daily totals
- Top 5 expenses
- AI-generated insights and spending patterns

### 3. **LangGraph Integration**
- Multi-turn agentic workflow
- Tool calling for expense processing, logging, and analytics
- Persistent thread-based conversation state (SQLite)
- Integration with Google Gemini API



## Setup Instructions

### 1. Environment Config
Create a `.env` file in the project root:

```env
# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS_PATH=path_to_json_key_file

# Database
DB_PATH=expenses.db
DB_URL=sqlite:///expenses.db
GRAPH_STATE_DB=graph_state.db

# LangGraph Config
DEFAULT_USER_ID=default_user
DEFAULT_THREAD_ID=default_thread
APP_TZ=Asia/Kolkata

# Logging
LOG_LEVEL=INFO

# Optional: LangChain tracing
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_key
# LANGCHAIN_PROJECT=your_project
# LANGCHAIN_ENDPOINT=domain_endpoint


```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API Server

**Development mode** (with auto-reload):
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```



## Code Architecture

### Request Flow
```
FastAPI Endpoint
    ↓
Pydantic Schema Validation
    ↓
Router Handler 
    ↓
LangGraph State Graph 
    ↓
LLM Agent + Tool Calling 
    ↓
Tools: Processor → Store → Analytics
    ↓
Database (SQLite)
    ↓
JSON Response (Pydantic)
```

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

All endpoints return proper HTTP status codes:
- **200** - Success
- **422** - Validation error (invalid request body)
- **500** - Server error with descriptive message


## Expense Categories

The system supports the following categories:
- Fuel
- Groceries
- Food & Dining
- Transport
- Shopping
- Bills
- Rent
- Health
- Travel
- Other

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_TZ` | Asia/Kolkata | User timezone for date parsing |
| `DB_PATH` | expenses.db | SQLite database file |
| `GRAPH_STATE_DB` | graph_state.db | LangGraph checkpoint database |
| `LOG_LEVEL` | INFO | Python logging level |
| `DEFAULT_USER_ID` | default_user | Fallback user ID |
| `DEFAULT_THREAD_ID` | default_thread | Fallback thread ID |


## Future Enhancements

TBD

