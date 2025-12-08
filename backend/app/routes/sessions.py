"""Sessions routes."""

from fastapi import APIRouter, HTTPException, status
from time import time
from nanoid import generate
from app.models import (
    Session,
    CreateSessionRequest,
    UpdateSessionRequest,
)
from app.services import db

router = APIRouter(prefix="/api/v1/sessions", tags=["Sessions"])

# Session ID generation: 10 characters
SESSION_ID_SIZE = 10
USER_ID_SIZE = 8
USER_COLORS = [
    "#22d3ee",
    "#a78bfa",
    "#f472b6",
    "#fbbf24",
    "#34d399",
    "#fb7185",
    "#60a5fa",
    "#c084fc",
    "#4ade80",
    "#f97316",
]
MAX_USERS_PER_SESSION = 10


def get_random_color(existing_colors: list[str]) -> str:
    """Get a random color that's not already used."""
    available = [c for c in USER_COLORS if c not in existing_colors]
    if available:
        import random

        return random.choice(available)
    return USER_COLORS[0]


def generate_user_name() -> str:
    """Generate a random user name."""
    adjectives = ["Swift", "Clever", "Bold", "Calm", "Eager"]
    nouns = ["Coder", "Dev", "Hacker", "Builder", "Creator"]
    import random

    return f"{random.choice(adjectives)}{random.choice(nouns)}"


@router.post("", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session(request: CreateSessionRequest | None = None):
    """Create a new interview session.

    Returns:
        The newly created session
    """
    session_id = generate(alphabet="0123456789abcdefghijklmnopqrstuvwxyz", size=SESSION_ID_SIZE)
    created_at = int(time() * 1000)

    default_code = '// Start coding here\nconsole.log("Hello, World!");'
    code = request.code if request else default_code
    language = request.language if request else "javascript"

    session = db.create_session(session_id, language, code, created_at)
    return session


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Get session details.

    Args:
        session_id: The session ID

    Returns:
        The session details

    Raises:
        HTTPException: If session not found
    """
    session = db.get_session_by_id(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "SESSION_NOT_FOUND",
                "message": f"Session with ID '{session_id}' not found",
                "statusCode": 404,
            },
        )
    return session


@router.patch("/{session_id}", response_model=Session)
async def update_session(session_id: str, request: UpdateSessionRequest):
    """Update a session.

    Args:
        session_id: The session ID
        request: Update request with optional code, language, and status

    Returns:
        The updated session

    Raises:
        HTTPException: If session not found or invalid request
    """
    session = db.get_session_by_id(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "SESSION_NOT_FOUND",
                "message": f"Session with ID '{session_id}' not found",
                "statusCode": 404,
            },
        )

    # Check if at least one field is provided
    if request.code is None and request.language is None and request.status is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "INVALID_REQUEST",
                "message": "At least one field (code, language, or status) must be provided",
                "statusCode": 400,
            },
        )

    updated_session = db.update_session(
        session_id,
        code=request.code,
        language=request.language,
        status=request.status,
    )
    return updated_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    """Delete a session.

    Args:
        session_id: The session ID

    Raises:
        HTTPException: If session not found
    """
    if not db.delete_session(session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "SESSION_NOT_FOUND",
                "message": f"Session with ID '{session_id}' not found",
                "statusCode": 404,
            },
        )
