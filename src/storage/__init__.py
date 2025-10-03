"""
Storage layer package for data persistence.

This package provides data access and persistence functionality for the application.
Currently implements in-memory storage for development and testing purposes.

Modules:
    memory: In-memory storage implementation for patient data using Python dictionaries.

Future implementations may include:
    - Database backends (PostgreSQL, MySQL, etc.)
    - File-based storage
    - Cache layers (Redis, Memcached)
    - External API integrations

The storage layer abstracts the persistence mechanism from business logic,
allowing for easy switching between different storage backends without
affecting the rest of the application.
"""
