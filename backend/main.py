"""Entry point for the FastAPI application."""

import uvicorn
from app import create_app


def main():
    """Run the FastAPI application."""
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
