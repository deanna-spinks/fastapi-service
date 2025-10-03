"""
Utilities package for common helper functions.

This package contains reusable utility functions and helpers that are used
across different parts of the application. These utilities provide common
functionality that doesn't fit into specific domain layers.

Modules:
    id_generator: Sequential ID generation for in-memory storage. Provides
                  a simple counter-based ID generator for creating unique
                  identifiers for stored entities.

Future utilities may include:
    - Date/time formatting helpers
    - Data validation utilities
    - String manipulation functions
    - Logging helpers
    - Configuration utilities
    - Cryptographic functions (hashing, encryption)

The utils package keeps cross-cutting concerns separate from business logic,
making them easily accessible and testable throughout the application.
"""
