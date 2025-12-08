# CodeInterview Backend API

FastAPI backend for the real-time collaborative code interview platform.

## Features

- **Session Management**: Create, join, and manage interview sessions
- **User Management**: Multiple users per session (up to 10)
- **Code Execution**: Execute Python code with sandboxing (JavaScript/TypeScript browser-only)
- **Real-time Collaboration**: Support for multiple users editing and executing code simultaneously

## Project Structure

```
app/
├── models/           # Pydantic models and schemas
├── routes/           # API endpoints
│   ├── sessions.py   # Session CRUD operations
│   ├── users.py      # User management endpoints
│   ├── execution.py  # Code execution endpoints
│   └── health.py     # Health check endpoint
└── services/         # Business logic
    ├── database.py   # Mock database implementation
    └── execution.py  # Code execution service

tests/               # Comprehensive test suite
├── conftest.py     # Pytest fixtures
├── test_sessions.py       # Session tests
├── test_users.py          # User tests
├── test_execution.py      # Execution tests
├── test_health.py         # Health check tests
└── test_integration.py    # Integration tests
```

## Quick Start

### Installation

```bash
# Install dependencies (requires uv)
pip install -e ".[dev]"
```

### Running the Server

```bash
# Start the development server
python main.py
```

The API will be available at `http://localhost:8000`

### Running Tests

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_sessions.py -v

# Run with coverage
python -m pytest tests/ --cov=app
```

## API Endpoints

### Sessions
- `POST /api/v1/sessions` - Create a new session
- `GET /api/v1/sessions/{session_id}` - Get session details
- `PATCH /api/v1/sessions/{session_id}` - Update session
- `DELETE /api/v1/sessions/{session_id}` - Delete session

### Users
- `POST /api/v1/sessions/{session_id}/users` - Join session
- `GET /api/v1/sessions/{session_id}/users` - Get session users
- `DELETE /api/v1/sessions/{session_id}/users/{user_id}` - Leave session

### Code Execution
- `POST /api/v1/execute` - Execute code

### Health
- `GET /api/v1/health` - Health check

## API Documentation

Once the server is running, view interactive documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

The project includes 43 comprehensive tests covering:
- **Session Operations**: Create, read, update, delete
- **User Management**: Join, leave, capacity limits
- **Code Execution**: Python execution, error handling, JavaScript/TypeScript message
- **Health Checks**: API availability
- **Integration Tests**: Complete user workflows

### Test Coverage

```
- test_sessions.py: 14 tests
- test_users.py: 14 tests
- test_execution.py: 11 tests
- test_health.py: 2 tests
- test_integration.py: 5 tests
```

All tests pass with no warnings ✓

## Database

Currently uses an in-memory mock database. To replace with a real database:

1. Create a new database service in `app/services/`
2. Implement the same interface as `MockDatabase`
3. Update imports in route files

## Code Execution Security

Currently:
- **Python**: Limited to safe built-in functions (print, len, range, etc.)
- **JavaScript/TypeScript**: Message recommending browser execution
- **No external imports**: Prevents arbitrary code execution

For production, consider:
- Docker containers for code execution
- RestrictedPython for additional safety
- Node.js runtime for JavaScript/TypeScript

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- python-nanoid: ID generation
- pytest: Testing framework

See `pyproject.toml` for version details.

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Format code (when tooling is added)
# black app tests

# Lint (when tooling is added)
# pylint app
```

## Future Enhancements

- Real database integration (PostgreSQL/MongoDB)
- WebSocket support for real-time updates
- User authentication and authorization
- Session persistence and history
- Advanced code sandbox with Docker
- Code execution timeouts and limits
- Cursor position tracking
- Collaborative debugging features
