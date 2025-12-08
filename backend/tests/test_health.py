"""Tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check_success(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_health_check_timestamp_format(self, client: TestClient):
        """Test that timestamp is in ISO format."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

        data = response.json()
        # Should be valid ISO format with Z suffix
        assert data["timestamp"].endswith("Z")

        # Try to parse it
        timestamp_str = data["timestamp"].replace("Z", "+00:00")
        try:
            datetime.fromisoformat(timestamp_str)
        except ValueError:
            pytest.fail("Timestamp is not valid ISO format")
