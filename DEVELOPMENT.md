# Development Setup & Running the App

## Quick Start - Run Everything at Once

From the root directory, run both frontend and backend with:

```bash
npm run dev
```

This will start:
- **Backend**: FastAPI server at `http://localhost:8000`
- **Frontend**: React dev server at `http://localhost:5173` (or configured port)

The frontend will automatically connect to the backend API.

## Individual Commands

### Backend Only
```bash
cd backend
source .venv/bin/activate
python main.py
```

The API will be available at:
- Main API: `http://localhost:8000/api/v1`
- Auto-docs (Swagger): `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Frontend Only
```bash
cd frontend
npm run dev
```

### Run Tests

**All backend tests:**
```bash
npm run test:backend
```

**Frontend linting:**
```bash
npm run test:frontend
```

## Project Structure

```
code-collab-hub/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/       # Pydantic models
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   └── __init__.py   # FastAPI app factory
│   ├── tests/            # Test suite (43 tests)
│   ├── main.py           # Entry point
│   ├── pyproject.toml    # Dependencies
│   └── .venv/            # Virtual environment
├── frontend/             # React + TypeScript
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks (useSession, useCodeExecution)
│   │   ├── services/     # API client
│   │   ├── pages/        # Page components
│   │   └── types/        # TypeScript types
│   ├── package.json      # Dependencies
│   └── vite.config.ts    # Vite config
├── package.json          # Root scripts
└── README.md             # This file
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Run backend + frontend concurrently |
| `npm run dev:backend` | Backend only |
| `npm run dev:frontend` | Frontend only |
| `npm run build` | Build frontend for production |
| `npm run test:backend` | Run backend tests (43 tests) |
| `npm run test:frontend` | Run frontend linting |

## Features

✅ Create collaborative code interview sessions
✅ Multi-user code editing (up to 10 users per session)
✅ Real-time code execution (Python, JavaScript, TypeScript)
✅ Monaco Editor with syntax highlighting
✅ Session sharing via URL
✅ User list with color coding
✅ Output panel for code results

## API Endpoints

See [API_ANALYSIS.md](./API_ANALYSIS.md) for full OpenAPI specification.

### Core Endpoints:
- **Sessions**: `POST/GET/PATCH/DELETE /api/v1/sessions`
- **Users**: `POST/GET/DELETE /api/v1/sessions/{id}/users`
- **Execution**: `POST /api/v1/execute`
- **Health**: `GET /api/v1/health`

## Technology Stack

**Backend:**
- FastAPI 0.109+
- Uvicorn 0.27+
- Pydantic 2.6+
- Python-nanoid 4.0+
- pytest 7.4+ with async support

**Frontend:**
- React 18.3.1
- TypeScript 5.8.3
- Vite 5.4.19
- React Router 6.30.1
- TanStack React Query 5.83.0
- Monaco Editor 4.6.0
- Shadcn/ui + Radix UI

## Troubleshooting

### Backend fails to start
- Ensure Python 3.12+ is installed
- Check virtual environment: `source backend/.venv/bin/activate`
- Verify dependencies: `python -m pip install -r backend/requirements.txt`

### Frontend shows "Initializing session..."
- Ensure backend is running at `http://localhost:8000`
- Check browser console for API errors
- Verify `VITE_API_URL` environment variable if needed

### Port conflicts
- Backend default: `8000`
- Frontend default: `5173`
- Modify in `backend/main.py` or `frontend/vite.config.ts` as needed

## Next Steps

- Implement real-time updates via WebSocket
- Add authentication/authorization
- Replace mock database with real database
- Add rate limiting and security hardening
- Deploy to production (Docker, Kubernetes)
