"""Tests for users endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestJoinSession:
    """Tests for joining sessions."""

    def test_join_session_success(self, client: TestClient):
        """Test joining a session."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Join session
        response = client.post(f"/api/v1/sessions/{session_id}/users")
        assert response.status_code == 201

        data = response.json()
        assert data["id"]
        assert len(data["id"]) == 8
        assert data["name"]
        assert data["color"]
        assert data["color"].startswith("#")
        assert "joinedAt" in data

    def test_join_session_with_name(self, client: TestClient):
        """Test joining a session with custom name."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.post(
            f"/api/v1/sessions/{session_id}/users", json={"name": "TestUser"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "TestUser"

    def test_join_session_not_found(self, client: TestClient):
        """Test joining a non-existent session."""
        response = client.post("/api/v1/sessions/nonexistent/users")
        assert response.status_code == 404

    def test_join_session_at_capacity(self, client: TestClient):
        """Test joining a session that's at capacity."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Join 10 users
        for i in range(10):
            response = client.post(f"/api/v1/sessions/{session_id}/users")
            assert response.status_code == 201

        # Try to join 11th user
        response = client.post(f"/api/v1/sessions/{session_id}/users")
        assert response.status_code == 409
        assert response.json()["detail"]["error"] == "SESSION_AT_CAPACITY"

    def test_join_session_multiple_users(self, client: TestClient):
        """Test multiple users joining the same session."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        user_ids = []
        for i in range(3):
            response = client.post(f"/api/v1/sessions/{session_id}/users")
            assert response.status_code == 201
            user_ids.append(response.json()["id"])

        # Verify all users have different IDs
        assert len(set(user_ids)) == 3

        # Verify different colors
        colors = []
        for user_id in user_ids:
            response = client.get(f"/api/v1/sessions/{session_id}/users")
            users = response.json()["users"]
            colors.extend([u["color"] for u in users])

        # Should have unique colors
        assert len(set(colors)) >= 3


class TestGetSessionUsers:
    """Tests for getting session users."""

    def test_get_session_users_empty(self, client: TestClient):
        """Test getting users from empty session."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.get(f"/api/v1/sessions/{session_id}/users")
        assert response.status_code == 200

        data = response.json()
        assert data["users"] == []

    def test_get_session_users_multiple(self, client: TestClient):
        """Test getting multiple users from a session."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Join 3 users
        for _ in range(3):
            client.post(f"/api/v1/sessions/{session_id}/users")

        response = client.get(f"/api/v1/sessions/{session_id}/users")
        assert response.status_code == 200

        data = response.json()
        assert len(data["users"]) == 3

        for user in data["users"]:
            assert user["id"]
            assert user["name"]
            assert user["color"]
            assert user["joinedAt"]

    def test_get_session_users_not_found(self, client: TestClient):
        """Test getting users from non-existent session."""
        response = client.get("/api/v1/sessions/nonexistent/users")
        assert response.status_code == 404


class TestLeaveSession:
    """Tests for leaving sessions."""

    def test_leave_session_success(self, client: TestClient):
        """Test leaving a session."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Join user
        join_response = client.post(f"/api/v1/sessions/{session_id}/users")
        user_id = join_response.json()["id"]

        # Leave session
        response = client.delete(f"/api/v1/sessions/{session_id}/users/{user_id}")
        assert response.status_code == 204

        # Verify user is removed
        get_response = client.get(f"/api/v1/sessions/{session_id}/users")
        assert len(get_response.json()["users"]) == 0

    def test_leave_session_not_found_session(self, client: TestClient):
        """Test leaving a non-existent session."""
        response = client.delete("/api/v1/sessions/nonexistent/users/user123")
        assert response.status_code == 404

    def test_leave_session_not_found_user(self, client: TestClient):
        """Test leaving as a non-existent user."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/sessions/{session_id}/users/nonexistent")
        assert response.status_code == 404

    def test_leave_session_multiple_users(self, client: TestClient):
        """Test one user leaving while others remain."""
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Join 3 users
        user_ids = []
        for _ in range(3):
            join_response = client.post(f"/api/v1/sessions/{session_id}/users")
            user_ids.append(join_response.json()["id"])

        # First user leaves
        response = client.delete(f"/api/v1/sessions/{session_id}/users/{user_ids[0]}")
        assert response.status_code == 204

        # Verify 2 users remain
        get_response = client.get(f"/api/v1/sessions/{session_id}/users")
        assert len(get_response.json()["users"]) == 2

        # Verify correct users remain
        remaining_ids = [u["id"] for u in get_response.json()["users"]]
        assert user_ids[1] in remaining_ids
        assert user_ids[2] in remaining_ids
