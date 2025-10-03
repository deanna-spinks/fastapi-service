"""
API layer package for the FastAPI application.

This package contains all API-related code including route definitions,
request handlers, and endpoint logic. The API layer follows a separation
of concerns pattern with two main subpackages:

Subpackages:
    routes: FastAPI router definitions with endpoint decorators and path operations.
            Routes handle request/response definitions and delegate business logic
            to handlers.

    handlers: Business logic for processing API requests. Handlers coordinate
              between the storage layer and API routes, perform validation,
              error handling, and data transformation.

Architecture:
    Client Request → Route (endpoint definition) → Handler (business logic)
    → Storage Layer (data persistence) → Handler → Route → Client Response

This separation allows for:
    - Clear separation between HTTP concerns and business logic
    - Easier testing (handlers can be tested independently)
    - Better code organization and maintainability
    - Reusability of business logic across different endpoints
"""
