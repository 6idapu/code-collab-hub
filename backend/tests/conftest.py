"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from app import create_app
from app.services import db


@pytest.fixture
def client():
    """Create a test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Clear the database before each test."""
    db.clear()
    yield
    db.clear()
