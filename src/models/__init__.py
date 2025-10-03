"""
Models package for data schemas and validation.

This package contains Pydantic models that define the data structures
and validation rules used throughout the application. These models serve
multiple purposes: request/response schemas for API endpoints, data
validation, and serialization/deserialization.

Modules:
    patients: Patient data models following the common pattern:
        - PatientCreate: Schema for creating new patients (API input)
        - PatientRead: Schema for returning patient data (API output)
        - PatientUpdate: Schema for partial updates (PATCH requests)
        - PatientInDB: Internal model with additional fields (created_at, updated_at)

Model Patterns:
    - Create models: Used for POST requests, contain required fields only
    - Read models: Used for API responses, include all client-visible fields
    - Update models: Used for PATCH/PUT requests, all fields optional
    - InDB models: Used internally, include storage-specific fields not exposed to
    clients

Benefits:
    - Automatic validation via Pydantic
    - Type safety and IDE autocomplete
    - Clear API contracts and documentation
    - Separation between internal and external representations
    - Easy serialization to/from JSON
"""
