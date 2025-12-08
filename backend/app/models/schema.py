from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


Language = Literal["javascript", "typescript", "python"]
SessionStatus = Literal["active", "completed"]


class User(BaseModel):
    """User model representing a participant in a session."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "user1234",
                "name": "SwiftCoder",
                "color": "#22d3ee",
                "joinedAt": 1702000000000,
            }
        }
    )

    id: str = Field(..., description="Unique user identifier (8 chars)")
    name: str = Field(..., description="User's display name")
    color: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$", description="Hex color code")
    joinedAt: int = Field(..., description="Unix timestamp when user joined")


class Session(BaseModel):
    """Session model representing an interview session."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "abcdef1234",
                "code": 'console.log("Hello, World!");',
                "language": "javascript",
                "users": [],
                "createdAt": 1702000000000,
                "status": "active",
            }
        }
    )

    id: str = Field(..., description="Unique session identifier (10 chars)")
    code: str = Field(..., description="Current code in the session")
    language: Language = Field(..., description="Programming language")
    users: list[User] = Field(default_factory=list, description="Users in the session")
    createdAt: int = Field(..., description="Unix timestamp when session was created")
    status: SessionStatus = Field(
        default="active", description="Current session status"
    )


class ExecutionResult(BaseModel):
    """Result of code execution."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"output": "Hello, World!", "error": None, "executionTime": 2.5}
        }
    )

    output: str = Field(..., description="Console output from code execution")
    error: str | None = Field(None, description="Error message if execution failed")
    executionTime: float = Field(
        ..., description="Time taken to execute code in milliseconds"
    )


class Error(BaseModel):
    """Error response model."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "INVALID_REQUEST",
                "message": "Invalid request parameters",
                "statusCode": 400,
            }
        }
    )

    error: str = Field(..., description="Error code or type")
    message: str = Field(..., description="Human-readable error message")
    statusCode: int = Field(..., description="HTTP status code")


class CreateSessionRequest(BaseModel):
    """Request to create a new session."""

    language: Language = Field(default="javascript", description="Programming language")
    code: str = Field(
        default='// Start coding here\nconsole.log("Hello, World!");',
        description="Initial code content",
    )


class UpdateSessionRequest(BaseModel):
    """Request to update a session."""

    code: str | None = Field(None, description="Updated code content")
    language: Language | None = Field(None, description="Updated programming language")
    status: SessionStatus | None = Field(None, description="Updated session status")


class JoinSessionRequest(BaseModel):
    """Request to join a session."""

    name: str | None = Field(None, description="User's display name")


class ExecuteCodeRequest(BaseModel):
    """Request to execute code."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 'console.log("Hello, World!");',
                "language": "javascript",
                "timeout": 30000,
            }
        }
    )

    code: str = Field(..., description="Code to execute")
    language: Language = Field(..., description="Programming language")
    timeout: int = Field(default=30000, description="Execution timeout in milliseconds")


class UsersResponse(BaseModel):
    """Response containing list of users."""

    users: list[User] = Field(..., description="List of users in the session")
