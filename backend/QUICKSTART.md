# Quick Start Guide - CodeInterview Backend

## Prerequisites
- Python 3.12+
- Virtual environment (`.venv`)
- Dependencies installed via `uv`

## Installation & Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Activate virtual environment (if using .venv)
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### 3. Start the development server
```bash
python main.py
```

The server will start on `http://localhost:8000`

### 4. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_sessions.py -v

# Run specific test class
python -m pytest tests/test_sessions.py::TestCreateSession -v

# Run with coverage
python -m pytest tests/ --cov=app
```

## API Endpoints

### Sessions
- `POST /api/v1/sessions` - Create new session
- `GET /api/v1/sessions/{sessionId}` - Get session
- `PATCH /api/v1/sessions/{sessionId}` - Update session
- `DELETE /api/v1/sessions/{sessionId}` - Delete session

### Users
- `POST /api/v1/sessions/{sessionId}/users` - Join session
- `GET /api/v1/sessions/{sessionId}/users` - Get users
- `DELETE /api/v1/sessions/{sessionId}/users/{userId}` - Leave session

### Code Execution
- `POST /api/v1/execute` - Execute code

### Health
- `GET /api/v1/health` - Health check

## Example API Requests

### Create a Session
```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello, World!\")"
  }'
```

### Join a Session
```bash
curl -X POST http://localhost:8000/api/v1/sessions/{sessionId}/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Developer1"}'
```

### Execute Code
```bash
curl -X POST http://localhost:8000/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(2 + 2)",
    "language": "python"
  }'
```

## Project Structure
```
backend/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py        # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── sessions.py      # Session endpoints
│   │   ├── users.py         # User endpoints
│   │   ├── execution.py     # Code execution
│   │   └── health.py        # Health check
│   └── services/
│       ├── __init__.py
│       ├── database.py      # Mock database
│       └── execution.py     # Code execution logic
├── tests/                   # Test suite (43 tests)
├── main.py                  # Entry point
├── pyproject.toml           # Dependencies
├── pytest.ini               # Test config
└── IMPLEMENTATION.md        # Detailed docs
```

## Troubleshooting

### Port Already in Use
```bash
python main.py  # Use different port if needed
# Or kill process on port 8000:
lsof -ti:8000 | xargs kill -9  # macOS/Linux
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
python -m venv .venv
source .venv/bin/activate  # or appropriate for your OS
pip install -e .
```

### Test Failures
```bash
# Run with verbose output
python -m pytest tests/ -vv

# Run single test for debugging
python -m pytest tests/test_sessions.py::TestCreateSession::test_create_session_default_values -vv
```

## Development Notes

- **Database**: Currently uses in-memory mock database (data persists during session)
- **Code Execution**: 
  - Python: Executed in sandbox with restricted built-ins
  - JavaScript/TypeScript: Returns message (browser execution recommended)
- **Session Capacity**: Max 10 users per session
- **Auto-generated IDs**: Uses nanoid for unique identifiers
- **Timestamps**: Unix milliseconds for consistency with frontend

## Next Steps

1. Replace mock database with PostgreSQL/MongoDB
2. Add WebSocket support for real-time updates
3. Implement authentication/authorization
4. Add code execution sandbox (Docker)
5. Deploy to cloud platform

## Support

For issues or questions, refer to:
- [OpenAPI Specification](../openapi.yaml)
- [API Analysis](../API_ANALYSIS.md)
- [Endpoint Reference](../ENDPOINT_REFERENCE.md)
- [Implementation Details](./IMPLEMENTATION.md)
