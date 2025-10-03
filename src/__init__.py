"""
FastAPI Patient Management Service - Source Code

This package contains the core application code organized in a layered architecture
pattern that separates concerns and promotes maintainability.

Architecture Flow:
    Request → routes (endpoint definitions) → handlers (business logic)
    → storage (data persistence) ← models (validation)

    Cross-cutting concerns are handled by utils (helpers, ID generation, etc.)

Package Structure:
    api/
        routes/       - FastAPI router definitions with endpoint decorators
        handlers/     - Business logic coordinating between storage and routes

    models/           - Pydantic schemas for request/response validation
                        (Create, Read, Update, InDB patterns)

    storage/          - Data persistence layer (currently in-memory)
                        Abstracted to allow swapping implementations

    utils/            - Shared utilities (ID generation, helpers)

    main.py           - FastAPI app instance and application entry point

Design Principles:
    - Separation of Concerns: Each layer has a single responsibility
    - Dependency Flow: Outer layers depend on inner layers, not vice versa
    - Type Safety: Pydantic models provide runtime validation and type hints
    - Abstraction: Storage layer can be swapped without changing business logic
    - Testability: Each layer can be tested independently

Adding New Endpoints:
    1. Define Pydantic models in models/
    2. Add route definitions in api/routes/
    3. Implement business logic in api/handlers/
    4. Add storage operations in storage/
    5. Register router in main.py
"""
