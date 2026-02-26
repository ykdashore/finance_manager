# Test Suite - Finance Manager

```
tests/
├── test_processor.py        # Expense data validation & fixes
├── test_schemas.py          # Request/response schema validation
├── test_store.py            # Database operations
├── test_analytics.py        # Weekly report calculations
├── test_api_chat.py         # Chat API endpoints
├── test_api_analytics.py    # Analytics API endpoints
├── conftest.py              # Shared fixtures
└── README.md                # This file
```

## Run Tests

### Install dependencies:
```bash
pip install -r requirements-dev.txt
```

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=app
```

### Run specific test file:
```bash
pytest tests/test_processor.py -v
```
