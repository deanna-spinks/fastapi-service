"""
API exception handling utilities.

This module provides utilities for converting domain-level exceptions
(e.g., ValueError) into appropriate HTTP exceptions (e.g., HTTPException)
for consistent API error responses.
"""

from fastapi import HTTPException


def handle_not_found_error(e: ValueError) -> None:
    """
    Convert 'not found' ValueError to HTTPException 404.
    
    If the ValueError message contains 'not found' (case insensitive),
    converts it to an HTTPException with 404 status code.
    Otherwise, re-raises the original ValueError.
    
    This helper standardizes error handling across API handlers, ensuring
    consistent 404 responses when domain operations fail to find resources.
    
    Args:
        e: The ValueError to handle
        
    Raises:
        HTTPException: 404 if error message contains 'not found'
        ValueError: Re-raises original error if not a 'not found' error
    
    Examples:
        >>> try:
        ...     # Domain operation that raises ValueError
        ...     raise ValueError("Patient with id 1 not found")
        ... except ValueError as e:
        ...     handle_not_found_error(e)
        HTTPException: 404 Patient with id 1 not found
        
        >>> try:
        ...     raise ValueError("Database connection failed")
        ... except ValueError as e:
        ...     handle_not_found_error(e)
        ValueError: Database connection failed
    """
    if "not found" in str(e).lower():
        raise HTTPException(status_code=404, detail=str(e))
    raise e
