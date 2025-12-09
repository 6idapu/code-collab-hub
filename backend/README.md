# CodeInterview Backend

FastAPI backend for the CodeInterview collaborative code interview platform.

## Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (`.venv`) activated

### 1. Start the Server
```bash
python main.py
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Run Tests
```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_sessions.py -v

# With coverage
python -m pytest tests/ --cov=app
```

## API Endpoints

### Sessions
- `POST /api/v1/sessions` - Create session
- `GET /api/v1/sessions/{sessionId}` - Get session
- `PATCH /api/v1/sessions/{sessionId}` - Update session
- `DELETE /api/v1/sessions/{sessionId}` - Delete session

### Users
- `POST /api/v1/sessions/{sessionId}/users` - Join session
- `GET /api/v1/sessions/{sessionId}/users` - Get users
- `DELETE /api/v1/sessions/{sessionId}/users/{userId}` - Leave session

### Code Execution
- `POST /api/v1/execute` - Execute code (Python/JavaScript/TypeScript)

### Health
- `GET /api/v1/health` - Health check

## Example API Requests

### Create a Session
```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "code": "print(\"Hello\")"}'
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
  -d '{"code": "print(2 + 2)", "language": "python"}'
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py              # FastAPI app factory
│   ├── models/
│   │   └── schema.py            # Pydantic models
│   ├── routes/
│   │   ├── sessions.py          # Session endpoints
│   │   ├── users.py             # User endpoints
│   │   ├── execution.py         # Code execution
│   │   └── health.py            # Health check
│   └── services/
│       ├── database.py          # Mock in-memory database
│       └── execution.py         # Code execution logic
├── tests/                       # Test suite (43 tests)
├── main.py                      # Entry point
├── pyproject.toml               # Dependencies
└── IMPLEMENTATION.md            # Detailed architecture
```

## Features

✅ **Session Management**
- Create, update, delete sessions
- Support for JavaScript, TypeScript, Python
- Session status tracking (active/completed)

✅ **User Management**
- Join/leave sessions
- Max 10 users per session
- Auto-assigned colors and names

✅ **Code Execution**
- Python: Sandboxed execution
- JavaScript/TypeScript: Browser execution recommended
- Execution time tracking

✅ **Test Coverage**
- 43 unit & integration tests
- Happy path and error scenarios
- Capacity limits and edge cases

## Configuration

The API uses:
- **Database**: PostgreSQL is the default in production; set `DATABASE_URL`.
  - For local development, `docker-compose up --build` includes a Postgres service and sets `DATABASE_URL` automatically.
  - You can still fallback to SQLite by setting `DATABASE_URL` to a sqlite URL like `sqlite:///./code_interview.db`.
- **Execution**: Python sandbox (JavaScript requires Node.js runtime)
- **CORS**: Enabled for all origins (restrict in `app/__init__.py` for production)

## Development

### Run with hot reload
```bash
python main.py
```

### Add dependencies
Update `pyproject.toml` and sync with `uv sync`

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
```

### Test Failures
```bash
python -m pytest tests/ -vv
```

### Virtual Environment Issues
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

## Next Steps

1. Replace mock database with PostgreSQL/MongoDB
2. Add WebSocket for real-time collaboration
3. Implement authentication
4. Add proper code execution sandbox (Docker)
5. Deploy to cloud

## References

- [OpenAPI Specification](../openapi.yaml)
- [API Analysis](../API_ANALYSIS.md)
- [Implementation Details](./IMPLEMENTATION.md)
