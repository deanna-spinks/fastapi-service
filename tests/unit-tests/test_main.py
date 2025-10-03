import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Test client for main app endpoints"""
    return TestClient(app)


@pytest.mark.unit
def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data


@pytest.mark.unit
def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "FastAPI Service is running"


@pytest.mark.unit
def test_api_documentation(client):
    """Test API documentation endpoints are available"""
    # Test Swagger UI endpoint
    response = client.get("/docs")
    assert response.status_code == 200

    # Test OpenAPI schema endpoint
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert "paths" in data
