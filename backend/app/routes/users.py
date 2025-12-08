"""Users routes."""

from fastapi import APIRouter, HTTPException, status
from time import time
from nanoid import generate
from app.models import User, JoinSessionRequest, UsersResponse
from app.services import db

router = APIRouter(prefix="/api/v1/sessions", tags=["Users"])

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


@router.post("/{session_id}/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def join_session(session_id: str, request: JoinSessionRequest | None = None):
    """Join a session.

    Args:
        session_id: The session ID
        request: Optional join request with user name

    Returns:
        The created user object

    Raises:
        HTTPException: If session not found or at capacity
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

    # Check capacity
    if len(session.users) >= MAX_USERS_PER_SESSION:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "SESSION_AT_CAPACITY",
                "message": f"Session has reached maximum of {MAX_USERS_PER_SESSION} users",
                "statusCode": 409,
            },
        )

    # Create user
    user_id = generate(alphabet="0123456789abcdefghijklmnopqrstuvwxyz", size=USER_ID_SIZE)
    user_name = (
        request.name if request and request.name else generate_user_name()
    )
    existing_colors = [u.color for u in session.users]
    color = get_random_color(existing_colors)
    joined_at = int(time() * 1000)

    user = User(id=user_id, name=user_name, color=color, joinedAt=joined_at)

    db.add_user(session_id, user)
    return user


@router.get("/{session_id}/users", response_model=UsersResponse)
async def get_session_users(session_id: str):
    """Get all users in a session.

    Args:
        session_id: The session ID

    Returns:
        List of users in the session

    Raises:
        HTTPException: If session not found
    """
    users = db.get_session_users(session_id)
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "SESSION_NOT_FOUND",
                "message": f"Session with ID '{session_id}' not found",
                "statusCode": 404,
            },
        )
    return UsersResponse(users=users)


@router.delete("/{session_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def leave_session(session_id: str, user_id: str):
    """Leave a session.

    Args:
        session_id: The session ID
        user_id: The user ID

    Raises:
        HTTPException: If session or user not found
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

    user = db.get_user_in_session(session_id, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "USER_NOT_FOUND",
                "message": f"User with ID '{user_id}' not found in session",
                "statusCode": 404,
            },
        )

    db.remove_user(session_id, user_id)
