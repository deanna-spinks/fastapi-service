"""Application configuration management using environment variables.

This module provides a centralized configuration management system using Pydantic
Settings.
All configuration is loaded from environment variables with sensible defaults.

Usage (Dependency Injection - Recommended):
    from fastapi import Depends
    from src.core.config import get_settings, Settings

    @app.get("/")
    def root(settings: Settings = Depends(get_settings)):
        return {"app_name": settings.app_name}

Usage (Direct Import - For startup/initialization only):
    from src.core.config import get_settings

    settings = get_settings()
    print(settings.app_name)
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = Field(
        default="FastAPI Patient Management Service",
        description="Application name",
    )
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="Environment name"
    )
    debug: bool = Field(default=True, description="Debug mode")
    app_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Application log level"
    )

    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(
        default=True, description="Auto-reload on code changes (development only)"
    )

    # Uvicorn settings
    uvicorn_workers: int = Field(
        default=1, description="Number of worker processes", ge=1
    )
    uvicorn_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="DEBUG", description="Uvicorn log level"
    )
    uvicorn_access_log: bool = Field(default=True, description="Enable access logs")

    # API settings
    api_prefix: str = Field(default="", description="API prefix for all routes")
    api_title: str = Field(
        default="Patient Management API", description="API documentation title"
    )
    api_description: str = Field(
        default="A modern microservice for patient management",
        description="API documentation description",
    )
    docs_url: str = Field(default="/docs", description="Swagger UI URL")
    redoc_url: str = Field(default="/redoc", description="ReDoc URL")
    openapi_url: str = Field(default="/openapi.json", description="OpenAPI schema URL")

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_environment(cls, v: str) -> str:
        """Normalize environment to lowercase."""
        if isinstance(v, str):
            return v.lower().strip()
        return v

    @field_validator("app_log_level", "uvicorn_log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, v: str) -> str:
        """Normalize log level to uppercase."""
        if isinstance(v, str):
            return v.upper().strip()
        return v

    @field_validator("debug", mode="after")
    @classmethod
    def validate_debug_in_production(cls, v: bool, info) -> bool:
        """Ensure debug is disabled in production."""
        if info.data.get("environment") == "production" and v:
            raise ValueError("Debug mode must be disabled in production")
        return v

    @field_validator("port", mode="after")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Ensure port is in valid range."""
        if not 1 <= v <= 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {v}")
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    This function is decorated with @lru_cache to ensure we only create
    one instance of Settings. Use this with FastAPI's Depends() for
    dependency injection in routes and handlers.

    Returns:
        Settings: Cached settings instance
    """
    return Settings()
