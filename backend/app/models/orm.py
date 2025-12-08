"""SQLAlchemy ORM models."""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between sessions and users
session_users = Table(
    'session_users',
    Base.metadata,
    Column('session_id', String(10), ForeignKey('sessions.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', String(8), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
)


class SessionModel(Base):
    """SQLAlchemy model for interview sessions."""
    __tablename__ = 'sessions'
    
    id = Column(String(10), primary_key=True)
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False, default='javascript')
    status = Column(String(20), nullable=False, default='active')
    created_at = Column(Integer, nullable=False)  # Unix timestamp in milliseconds
    updated_at = Column(Integer, nullable=False)  # Unix timestamp in milliseconds
    
    # Relationships
    users = relationship('UserModel', secondary=session_users, backref='sessions')
    
    def to_dict(self):
        """Convert to dictionary for Pydantic model."""
        return {
            'id': self.id,
            'code': self.code,
            'language': self.language,
            'status': self.status,
            'createdAt': self.created_at,
            'users': [u.to_dict() for u in self.users],
        }


class UserModel(Base):
    """SQLAlchemy model for users."""
    __tablename__ = 'users'
    
    id = Column(String(8), primary_key=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=False)
    joined_at = Column(Integer, nullable=False)  # Unix timestamp in milliseconds
    
    def to_dict(self):
        """Convert to dictionary for Pydantic model."""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'joinedAt': self.joined_at,
        }
