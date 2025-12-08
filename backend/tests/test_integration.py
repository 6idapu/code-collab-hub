"""Integration tests for the complete workflow."""

import pytest
from fastapi.testclient import TestClient


class TestCompleteWorkflow:
    """Tests for complete user workflows."""

    def test_create_session_and_join_multiple_users(self, client: TestClient):
        """Test complete workflow: create session and have users join."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        assert create_response.status_code == 201
        session_id = create_response.json()["id"]

        # Join first user
        user1_response = client.post(f"/api/v1/sessions/{session_id}/users")
        assert user1_response.status_code == 201
        user1_id = user1_response.json()["id"]

        # Join second user
        user2_response = client.post(f"/api/v1/sessions/{session_id}/users")
        assert user2_response.status_code == 201
        user2_id = user2_response.json()["id"]

        # Get session and verify both users are there
        get_response = client.get(f"/api/v1/sessions/{session_id}")
        assert get_response.status_code == 200
        session = get_response.json()
        assert len(session["users"]) == 2

        user_ids = [u["id"] for u in session["users"]]
        assert user1_id in user_ids
        assert user2_id in user_ids

    def test_create_session_update_code_execute(self, client: TestClient):
        """Test workflow: create, update code, and execute."""
        # Create session
        create_response = client.post("/api/v1/sessions")
        session_id = create_response.json()["id"]

        # Update code
        new_code = "print('test')"
        update_response = client.patch(
            f"/api/v1/sessions/{session_id}", json={"code": new_code}
        )
        assert update_response.status_code == 200
        assert update_response.json()["code"] == new_code

        # Execute the code
        exec_response = client.post(
            "/api/v1/execute", json={"code": new_code, "language": "python"}
        )
        assert exec_response.status_code == 200
        assert exec_response.json()["error"] is None

    def test_session_lifecycle(self, client: TestClient):
        """Test complete session lifecycle."""
        # 1. Create session
        create_response = client.post("/api/v1/sessions")
        assert create_response.status_code == 201
        session_id = create_response.json()["id"]
        assert create_response.json()["status"] == "active"

        # 2. Join users
        user1 = client.post(f"/api/v1/sessions/{session_id}/users").json()
        user2 = client.post(f"/api/v1/sessions/{session_id}/users").json()

        # 3. Get session and verify users
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert len(session["users"]) == 2

        # 4. Update code
        client.patch(
            f"/api/v1/sessions/{session_id}", json={"code": "print('hello')"}
        )

        # 5. User 1 leaves
        client.delete(f"/api/v1/sessions/{session_id}/users/{user1['id']}")
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert len(session["users"]) == 1

        # 6. Mark session as completed
        client.patch(
            f"/api/v1/sessions/{session_id}", json={"status": "completed"}
        )
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert session["status"] == "completed"

        # 7. User 2 leaves
        client.delete(f"/api/v1/sessions/{session_id}/users/{user2['id']}")
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert len(session["users"]) == 0

        # 8. Delete session
        response = client.delete(f"/api/v1/sessions/{session_id}")
        assert response.status_code == 204

        # Verify session is deleted
        response = client.get(f"/api/v1/sessions/{session_id}")
        assert response.status_code == 404

    def test_multiple_sessions_independent(self, client: TestClient):
        """Test that multiple sessions are independent."""
        # Create two sessions
        session1_id = client.post("/api/v1/sessions").json()["id"]
        session2_id = client.post("/api/v1/sessions").json()["id"]

        # Add users to each
        client.post(f"/api/v1/sessions/{session1_id}/users")
        client.post(f"/api/v1/sessions/{session2_id}/users")
        client.post(f"/api/v1/sessions/{session2_id}/users")

        # Verify session1 has 1 user
        session1 = client.get(f"/api/v1/sessions/{session1_id}").json()
        assert len(session1["users"]) == 1

        # Verify session2 has 2 users
        session2 = client.get(f"/api/v1/sessions/{session2_id}").json()
        assert len(session2["users"]) == 2

    def test_language_switching(self, client: TestClient):
        """Test switching languages in a session."""
        session_id = client.post("/api/v1/sessions").json()["id"]

        # Start with JavaScript
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert session["language"] == "javascript"

        # Switch to Python
        client.patch(
            f"/api/v1/sessions/{session_id}", json={"language": "python"}
        )
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert session["language"] == "python"

        # Switch to TypeScript
        client.patch(
            f"/api/v1/sessions/{session_id}", json={"language": "typescript"}
        )
        session = client.get(f"/api/v1/sessions/{session_id}").json()
        assert session["language"] == "typescript"
