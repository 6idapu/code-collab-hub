"""Tests for code execution endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestExecuteCode:
    """Tests for code execution."""

    def test_execute_python_code_success(self, client: TestClient):
        """Test executing Python code successfully."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "print('Hello, World!')", "language": "python"},
        )
        assert response.status_code == 200

        data = response.json()
        assert data["output"]
        assert data["error"] is None
        assert data["executionTime"] >= 0

    def test_execute_python_code_with_error(self, client: TestClient):
        """Test executing Python code with error."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "print(undefined_variable)", "language": "python"},
        )
        assert response.status_code == 200

        data = response.json()
        assert data["error"] is not None
        assert "NameError" in data["error"]

    def test_execute_python_syntax_error(self, client: TestClient):
        """Test executing Python code with syntax error."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "print('unclosed string", "language": "python"},
        )
        assert response.status_code == 200

        data = response.json()
        assert data["error"] is not None
        assert "SyntaxError" in data["error"]

    def test_execute_javascript_returns_message(self, client: TestClient):
        """Test executing JavaScript returns output."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "console.log('Hello')", "language": "javascript"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "Hello" in data["output"]
        assert data["error"] is None

    def test_execute_typescript_returns_message(self, client: TestClient):
        """Test executing TypeScript returns output."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "console.log('Hello')", "language": "typescript"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "Hello" in data["output"]
        assert data["error"] is None

    def test_execute_code_with_custom_timeout(self, client: TestClient):
        """Test executing code with custom timeout."""
        response = client.post(
            "/api/v1/execute",
            json={
                "code": "print('test')",
                "language": "python",
                "timeout": 5000,
            },
        )
        assert response.status_code == 200

    def test_execute_code_missing_code(self, client: TestClient):
        """Test executing without code field."""
        response = client.post(
            "/api/v1/execute", json={"language": "python"}
        )
        assert response.status_code == 422  # Validation error

    def test_execute_code_missing_language(self, client: TestClient):
        """Test executing without language field."""
        response = client.post("/api/v1/execute", json={"code": "print('test')"})
        assert response.status_code == 422  # Validation error

    def test_execute_python_arithmetic(self, client: TestClient):
        """Test executing Python arithmetic."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "print(2 + 2)", "language": "python"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "4" in data["output"]
        assert data["error"] is None

    def test_execute_python_multiple_lines(self, client: TestClient):
        """Test executing multiple lines of Python."""
        code = """for i in range(3):
    print(f'Iteration {i}')"""
        response = client.post(
            "/api/v1/execute",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "Iteration" in data["output"]
        assert data["error"] is None

    def test_execute_response_has_execution_time(self, client: TestClient):
        """Test that response includes execution time."""
        response = client.post(
            "/api/v1/execute",
            json={"code": "print('test')", "language": "python"},
        )
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data["executionTime"], (int, float))
        assert data["executionTime"] >= 0
