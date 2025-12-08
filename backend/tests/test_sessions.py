"""Tests for sessions endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestCreateSession:
    """Tests for creating sessions."""

    def test_create_session_default_values(self, client: TestClient):
        """Test creating a session with default values."""
        response = client.post("/api/v1/sessions")
        assert response.status_code == 201

        data = response.json()
        assert data["id"]
        assert len(data["id"]) == 10
        assert data["language"] == "javascript"
        assert data["code"] == '// Start coding here\nconsole.log("Hello, World!");'
        assert data["users"] == []
        assert data["status"] == "active"
        assert "createdAt" in data

    def test_create_session_custom_language(self, client: TestClient):
        """Test creating a session with custom language."""
        response = client.post(
            "/api/v1/sessions",
            json={"language": "python", "code": "print('Hello')"},
        )
        assert response.status_code == 201

        data = response.json()
        assert data["language"] == "python"
        assert data["code"] == "print('Hello')"

    def test_create_session_typescript(self, client: TestClient):
        """Test creating a session with TypeScript."""
        response = client.post(
            "/api/v1/sessions",
            json={"language": "typescript", "code": "console.log('test');"},
        )
        assert response.status_code == 201
        assert response.json()["language"] == "typescript"


class TestGetSession:
    """Tests for getting sessions."""

    def test_get_session_success(self, client: TestClient):
        """Test getting an existing session."""
        # Create session first
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Get session
        response = client.get(f"/api/v1/sessions/{session_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == session_id
        assert data["status"] == "active"

    def test_get_session_not_found(self, client: TestClient):
        """Test getting a non-existent session."""
        response = client.get("/api/v1/sessions/nonexistent")
        assert response.status_code == 404

        data = response.json()
        assert data["detail"]["error"] == "SESSION_NOT_FOUND"
        assert data["detail"]["statusCode"] == 404


class TestUpdateSession:
    """Tests for updating sessions."""

    def test_update_session_code(self, client: TestClient):
        """Test updating session code."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Update code
        new_code = "console.log('Updated!');"
        response = client.patch(
            f"/api/v1/sessions/{session_id}", json={"code": new_code}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["code"] == new_code

    def test_update_session_language(self, client: TestClient):
        """Test updating session language."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.patch(
            f"/api/v1/sessions/{session_id}", json={"language": "python"}
        )
        assert response.status_code == 200
        assert response.json()["language"] == "python"

    def test_update_session_status(self, client: TestClient):
        """Test updating session status."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.patch(
            f"/api/v1/sessions/{session_id}", json={"status": "completed"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_update_session_multiple_fields(self, client: TestClient):
        """Test updating multiple fields at once."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.patch(
            f"/api/v1/sessions/{session_id}",
            json={
                "code": "print('test')",
                "language": "python",
                "status": "completed",
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert data["code"] == "print('test')"
        assert data["language"] == "python"
        assert data["status"] == "completed"

    def test_update_session_not_found(self, client: TestClient):
        """Test updating a non-existent session."""
        response = client.patch(
            "/api/v1/sessions/nonexistent", json={"code": "test"}
        )
        assert response.status_code == 404

    def test_update_session_no_fields(self, client: TestClient):
        """Test updating with no fields raises error."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.patch(f"/api/v1/sessions/{session_id}", json={})
        assert response.status_code == 400


class TestDeleteSession:
    """Tests for deleting sessions."""

    def test_delete_session_success(self, client: TestClient):
        """Test deleting a session."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Delete session
        response = client.delete(f"/api/v1/sessions/{session_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/api/v1/sessions/{session_id}")
        assert get_response.status_code == 404

    def test_delete_session_not_found(self, client: TestClient):
        """Test deleting a non-existent session."""
        response = client.delete("/api/v1/sessions/nonexistent")
        assert response.status_code == 404
