"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.routes import sessions_router, users_router, execution_router, health_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="CodeInterview API",
        description="Real-time collaborative code interview platform API",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins (configure properly in production)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(sessions_router)
    app.include_router(users_router)
    app.include_router(execution_router)
    app.include_router(health_router)

    # Serve built frontend static files if present
    static_dir = Path(__file__).resolve().parent.parent / 'frontend' / 'dist'
    if static_dir.exists():
        # Mount the build at root so paths like '/assets' resolve correctly
        app.mount('/', StaticFiles(directory=str(static_dir), html=True), name='frontend')

    return app
