# CodeInterview Backend

FastAPI backend for the CodeInterview collaborative code interview platform.

## Features

- Real-time collaborative coding sessions
- Multi-user support (up to 10 users per session)
- Code execution for Python (with sandboxing)
- Session management
- Mock database (ready to replace with real database)

## Project Structure

```
backend/
├── app/
│   ├── models/          # Pydantic models and schemas
│   ├── routes/          # API route handlers
│   ├── services/        # Business logic (database, execution)
│   └── __init__.py      # FastAPI app factory
├── tests/               # Test suite
├── main.py              # Entry point
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## Installation

1. Install dependencies (using uv):
```bash
uv sync
```

2. Or using pip:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`
Alternative documentation (ReDoc): `http://localhost:8000/redoc`

## Running Tests

Run all tests:
```bash
uv run pytest
```

Run tests with verbose output:
```bash
uv run pytest -v
```

Run specific test file:
```bash
uv run pytest tests/test_sessions.py -v
```

Run tests with coverage:
```bash
uv run pytest --cov=app tests/
```

## API Endpoints

### Sessions
- `POST /api/v1/sessions` - Create a new session
- `GET /api/v1/sessions/{sessionId}` - Get session details
- `PATCH /api/v1/sessions/{sessionId}` - Update session
- `DELETE /api/v1/sessions/{sessionId}` - Delete session

### Users
- `POST /api/v1/sessions/{sessionId}/users` - Join a session
- `GET /api/v1/sessions/{sessionId}/users` - Get session users
- `DELETE /api/v1/sessions/{sessionId}/users/{userId}` - Leave session

### Code Execution
- `POST /api/v1/execute` - Execute code

### Health
- `GET /api/v1/health` - Health check

## Database

Currently uses a mock in-memory database. To replace with a real database:

1. Modify `app/services/database.py`
2. Update `MockDatabase` class to use your preferred ORM (SQLAlchemy, etc.)
3. Update connection strings and models

## Code Execution

The backend supports:
- **Python**: Executed in a restricted environment with limited built-ins
- **JavaScript/TypeScript**: Message returned suggesting browser execution

For production use, consider:
- Using a proper sandbox (Docker, VM)
- Adding timeout enforcement
- Rate limiting
- Resource limits

## Testing

Test coverage includes:
- **Unit tests**: Individual endpoint testing
- **Integration tests**: Complete workflows
- **Error handling**: Invalid inputs and edge cases

Test files:
- `tests/test_sessions.py` - Session endpoint tests
- `tests/test_users.py` - User endpoint tests
- `tests/test_execution.py` - Code execution tests
- `tests/test_health.py` - Health check tests
- `tests/test_integration.py` - Integration tests

## Development

### Adding a new dependency
```bash
uv add <package-name>
```

### Running in development mode
```bash
uv run python main.py
```

The server will reload on code changes thanks to Uvicorn's reload mode.

### Code style
Current codebase follows PEP 8 conventions. Consider adding:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

## Configuration

Environment variables (can be set in `.env`):
- `PYTHONUNBUFFERED=1` - Unbuffered Python output
- `HOST=0.0.0.0` - Server host
- `PORT=8000` - Server port

## Error Handling

The API returns standard HTTP status codes:
- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `404` - Not Found
- `409` - Conflict (e.g., session at capacity)
- `500` - Internal Server Error

Error responses include:
```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable message",
  "statusCode": 400
}
```

## CORS

The API includes CORS middleware allowing requests from all origins. For production, restrict this in `app/__init__.py`.

## License

See LICENSE file

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests to ensure they pass
4. Create a commit with descriptive message
5. Submit pull request
