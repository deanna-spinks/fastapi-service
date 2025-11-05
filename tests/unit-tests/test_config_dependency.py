"""Tests demonstrating how to test with dependency injection for settings.

This file shows the recommended pattern for testing endpoints that use
Settings as a dependency.
"""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.core.config import Settings, get_settings

# Test app setup
app = FastAPI()


@app.get("/test-endpoint")
def example_endpoint(settings: Settings = Depends(get_settings)):
    """Example endpoint that uses settings."""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
    }


@app.get("/production-check")
def production_check(settings: Settings = Depends(get_settings)):
    """Endpoint that behaves differently based on environment."""
    if settings.is_production:
        return {"message": "Running in production", "debug_enabled": False}
    return {"message": "Running in development", "debug_enabled": settings.debug}


# Fixtures
@pytest.fixture(autouse=True)
def clean_dependency_overrides():
    """Automatically clean up dependency overrides after each test."""
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """Provide a TestClient for the app."""
    return TestClient(app)


@pytest.fixture
def override_settings():
    """Provide a helper function to override settings in tests."""

    def _override(settings: Settings):
        app.dependency_overrides[get_settings] = lambda: settings
        return settings

    return _override


class TestSettingsDependencyInjection:
    """Test suite for settings dependency injection."""

    def test_default_settings(self, client):
        """Test endpoint with default settings."""
        response = client.get("/test-endpoint")

        assert response.status_code == 200
        data = response.json()
        assert "app_name" in data
        assert "environment" in data
        assert "debug" in data

    def test_override_settings_for_testing(self, client, override_settings):
        """Test with overridden settings."""
        # Create and override custom settings for testing
        override_settings(
            Settings(
                app_name="Test Application",
                environment="development",
                debug=True,
                port=9999,
            )
        )

        # Test with overridden settings
        response = client.get("/test-endpoint")

        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "Test Application"
        assert data["environment"] == "development"
        assert data["debug"] is True

    def test_production_environment(self, client, override_settings):
        """Test behavior in production environment."""
        override_settings(
            Settings(
                app_name="Production App",
                environment="production",
                debug=False,
            )
        )

        response = client.get("/production-check")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Running in production"
        assert data["debug_enabled"] is False

    def test_development_environment(self, client, override_settings):
        """Test behavior in development environment."""
        override_settings(
            Settings(
                app_name="Dev App",
                environment="development",
                debug=True,
            )
        )

        response = client.get("/production-check")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Running in development"
        assert data["debug_enabled"] is True

    def test_multiple_requests_use_same_settings(self, client, override_settings):
        """Verify that settings are cached across requests."""
        override_settings(Settings(app_name="Cached App"))

        response1 = client.get("/test-endpoint")
        response2 = client.get("/test-endpoint")

        assert response1.json()["app_name"] == "Cached App"
        assert response2.json()["app_name"] == "Cached App"


# Alternative: Specific settings fixture for reuse
@pytest.fixture
def test_settings():
    """Fixture that provides commonly used test settings."""
    return Settings(
        app_name="Test App via Fixture",
        environment="development",
        debug=True,
        app_log_level="DEBUG",
    )


def test_with_fixture(client, override_settings, test_settings):
    """Test using fixture-based settings override."""
    override_settings(test_settings)

    response = client.get("/test-endpoint")

    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "Test App via Fixture"
    assert data["environment"] == "development"


# Testing settings validation
class TestSettingsValidation:
    """Test settings validation rules."""

    def test_valid_settings(self):
        """Test that valid settings are accepted."""
        settings = Settings(
            environment="development",
            debug=True,
            port=8000,
        )
        assert settings.environment == "development"
        assert settings.debug is True

    def test_port_validation(self):
        """Test that invalid ports are rejected."""
        with pytest.raises(ValueError, match="Port must be between"):
            Settings(port=70000)

        with pytest.raises(ValueError, match="Port must be between"):
            Settings(port=0)

    def test_debug_in_production_validation(self):
        """Test that debug cannot be enabled in production."""
        with pytest.raises(
            ValueError, match="Debug mode must be disabled in production"
        ):
            Settings(environment="production", debug=True)

    def test_properties(self):
        """Test settings properties."""
        settings = Settings(environment="production", debug=False)
        assert settings.is_production is True
        assert settings.is_development is False

        settings = Settings(environment="development", debug=True)
        assert settings.is_production is False
        assert settings.is_development is True

    def test_log_level_normalization(self):
        """Test log level normalization to uppercase."""
        settings = Settings(app_log_level="debug", uvicorn_log_level="debug")
        assert settings.app_log_level == "DEBUG"
        assert settings.uvicorn_log_level == "DEBUG"

    def test_environment_normalization(self):
        """Test environment normalization to lowercase."""
        settings = Settings(environment="PRODUCTION", debug=False)
        assert settings.environment == "production"
