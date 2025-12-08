"""Mock database for sessions and users."""

from typing import Optional
from app.models import Session, User, Language, SessionStatus


class MockDatabase:
    """In-memory mock database for storing sessions and users."""

    def __init__(self):
        self.sessions: dict[str, Session] = {}

    # Session operations
    def create_session(
        self, session_id: str, language: Language, code: str, created_at: int
    ) -> Session:
        """Create a new session."""
        session = Session(
            id=session_id, code=code, language=language, users=[], createdAt=created_at
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        return self.sessions.get(session_id)

    def update_session(
        self,
        session_id: str,
        code: Optional[str] = None,
        language: Optional[Language] = None,
        status: Optional[SessionStatus] = None,
    ) -> Optional[Session]:
        """Update a session."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        if code is not None:
            session.code = code
        if language is not None:
            session.language = language
        if status is not None:
            session.status = status

        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self.sessions

    # User operations
    def add_user(self, session_id: str, user: User) -> Optional[Session]:
        """Add a user to a session."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        session.users.append(user)
        return session

    def get_session_users(self, session_id: str) -> Optional[list[User]]:
        """Get all users in a session."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        return session.users

    def remove_user(self, session_id: str, user_id: str) -> Optional[Session]:
        """Remove a user from a session."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        session.users = [u for u in session.users if u.id != user_id]
        return session

    def get_user_in_session(self, session_id: str, user_id: str) -> Optional[User]:
        """Get a specific user in a session."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        for user in session.users:
            if user.id == user_id:
                return user
        return None

    def clear(self):
        """Clear all sessions (for testing)."""
        self.sessions.clear()


# Global database instance
db = MockDatabase()
