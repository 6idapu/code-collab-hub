"""Health check routes."""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        Health status with timestamp
    """
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
