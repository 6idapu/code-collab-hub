"""SQLAlchemy database service."""

import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession
from app.models.orm import Base, SessionModel, UserModel
from app.models import Session, User, Language, SessionStatus


class Database:
    """SQLAlchemy database service for sessions and users."""

    def __init__(self, database_url: str = "sqlite:///./code_interview.db"):
        """Initialize database connection.
        
        Args:
            database_url: Database connection string (default: SQLite file)
        """
        self.engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
            echo=False,  # Set to True for SQL debugging
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> SQLSession:
        """Get a database session."""
        return self.SessionLocal()

    # Session operations
    def create_session(
        self, session_id: str, language: Language, code: str, created_at: int
    ) -> Session:
        """Create a new session."""
        db = self.get_session()
        try:
            session = SessionModel(
                id=session_id,
                code=code,
                language=language,
                created_at=created_at,
                updated_at=created_at,
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return Session(**session.to_dict())
        finally:
            db.close()

    def get_session_by_id(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if session:
                return Session(**session.to_dict())
            return None
        finally:
            db.close()

    def update_session(
        self,
        session_id: str,
        code: Optional[str] = None,
        language: Optional[Language] = None,
        status: Optional[SessionStatus] = None,
    ) -> Optional[Session]:
        """Update a session."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return None

            if code is not None:
                session.code = code
            if language is not None:
                session.language = language
            if status is not None:
                session.status = status
            
            session.updated_at = int(__import__('time').time() * 1000)
            db.commit()
            db.refresh(session)
            return Session(**session.to_dict())
        finally:
            db.close()

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return False
            
            db.delete(session)
            db.commit()
            return True
        finally:
            db.close()

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        db = self.get_session()
        try:
            return db.query(SessionModel).filter(SessionModel.id == session_id).first() is not None
        finally:
            db.close()

    # User operations
    def add_user(self, session_id: str, user: User) -> Optional[Session]:
        """Add a user to a session."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return None

            # Check if user already exists, if not create
            user_obj = db.query(UserModel).filter(UserModel.id == user.id).first()
            if not user_obj:
                user_obj = UserModel(
                    id=user.id,
                    name=user.name,
                    color=user.color,
                    joined_at=user.joinedAt,
                )
                db.add(user_obj)
            
            # Add user to session if not already there
            if user_obj not in session.users:
                session.users.append(user_obj)
            
            db.commit()
            db.refresh(session)
            return Session(**session.to_dict())
        finally:
            db.close()

    def get_session_users(self, session_id: str) -> Optional[list[User]]:
        """Get all users in a session."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return None
            return [User(**u.to_dict()) for u in session.users]
        finally:
            db.close()

    def remove_user(self, session_id: str, user_id: str) -> Optional[Session]:
        """Remove a user from a session."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return None

            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user and user in session.users:
                session.users.remove(user)
                db.commit()
            
            db.refresh(session)
            return Session(**session.to_dict())
        finally:
            db.close()

    def get_user_in_session(self, session_id: str, user_id: str) -> Optional[User]:
        """Get a specific user in a session."""
        db = self.get_session()
        try:
            session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if not session:
                return None

            for user in session.users:
                if user.id == user_id:
                    return User(**user.to_dict())
            return None
        finally:
            db.close()

    def clear(self):
        """Clear all sessions (for testing)."""
        db = self.get_session()
        try:
            db.query(SessionModel).delete()
            db.query(UserModel).delete()
            db.commit()
        finally:
            db.close()


# Global database instance
database_url = os.getenv("DATABASE_URL", "sqlite:///./code_interview.db")
db = Database(database_url)
