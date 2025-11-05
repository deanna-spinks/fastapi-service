from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI

from src.api.routes.patients import patients_router
from src.core.config import Settings, get_settings

settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.app_version,
    docs_url=settings.docs_url if settings.docs_url else None,
    redoc_url=settings.redoc_url if settings.redoc_url else None,
    openapi_url=settings.openapi_url if settings.openapi_url else None,
    debug=settings.debug,
)


def run():
    """Run the application with uvicorn."""
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload and settings.is_development,
        workers=settings.uvicorn_workers if not settings.reload else 1,
        log_level=settings.uvicorn_log_level,
        access_log=settings.uvicorn_access_log,
    )


@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    """Health check endpoint with service information.

    Uses dependency injection to get settings - this makes the endpoint
    testable and allows for settings overrides in tests.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/")
def root():
    return {"message": "FastAPI Service is running"}


app.include_router(patients_router)


if __name__ == "__main__":
    run()
