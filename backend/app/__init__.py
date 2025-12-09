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
        app.mount('/static', StaticFiles(directory=str(static_dir)), name='static')

        # Serve index.html for the root path and any non-API routes (SPA)
        @app.get('/', include_in_schema=False)
        def _root_index():
            return FileResponse(static_dir / 'index.html')

        @app.get('/{full_path:path}', include_in_schema=False)
        def _spa_index(full_path: str):
            # Don't override API or docs routes - let FastAPI return 404 or match other routers
            if full_path.startswith('api') or full_path.startswith('_') or full_path.startswith('docs'):
                from fastapi import HTTPException

                raise HTTPException(status_code=404)
            return FileResponse(static_dir / 'index.html')

    return app
