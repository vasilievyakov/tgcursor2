"""
API dependencies.
"""
from fastapi import Header, HTTPException, status
from typing import Optional


async def get_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Optional API key authentication for MVP.
    In production, implement proper authentication.
    """
    # For MVP, authentication is optional
    # In production, validate API key here
    return x_api_key

