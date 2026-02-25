# Finance Manager API

## Project Structure

```
finance_manager/
├── main.py                          # FastAPI application entry point
├── run_cli.py                       # CLI interface (alternative to API)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── app/
│   ├── __init__.py
│   ├── api/                         # API routers
│   │   ├── __init__.py
│   │   ├── chat.py                  # Chat endpoint router
│   │   └── analytics.py             # Analytics endpoint router
│   ├── core/                        # Core application logic
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration management
│   │   ├── prompts.py               # LLM system prompts
│   │   ├── state.py                 # LangGraph state definition
│   │   └── state_graph.py           # Compiled LangGraph agent
│   ├── db/                          # Database layer
│   │   ├── schema.sql               # SQLite schema
│   │   └── session.py               # SQLAlchemy session factory
│   ├── models/                      # Data models & schemas
│   │   ├── __init__.py
│   │   ├── entities.py              # SQLAlchemy ORM models
│   │   └── schemas.py               # Pydantic request/response schemas
│   └── tools/                       # LangGraph tools
│       ├── __init__.py
│       ├── processor.py             # Expense extraction & categorization
│       ├── store.py                 # Expense database operations
│       └── analytics.py             # Weekly reports & insights
└── agenticaiprep-3dea44180eb5.json  # Google Cloud credentials
```



