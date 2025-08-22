"""
Authentication Pydantic schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field

from .user import UserResponse


class Token(BaseModel):
    """Schema for authentication token response."""
    
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Schema for token data payload."""
    
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request."""
    
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    
    refresh_token: str = Field(..., min_length=1)
