"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

    return app
