"""
Authentication endpoints.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.auth import Token, LoginRequest
from app.core.logging import get_logger
from app.api.dependencies import get_current_user

logger = get_logger(__name__)

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate user and return access token.
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        Token: Access token response
        
    Raises:
        HTTPException: If authentication fails
    """
    user_service = UserService(db)
    user = user_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        logger.warning("Login failed: invalid credentials", email=login_data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    logger.info("User logged in successfully", user_id=user.id, email=user.email)
    
    return Token(access_token=access_token, token_type="bearer", user=user)


@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Token:
    """
    Refresh access token for current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Token: New access token response
    """
    # Create new access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        subject=current_user.id, expires_delta=access_token_expires
    )
    
    logger.info("Token refreshed successfully", user_id=current_user.id)
    
    return Token(access_token=access_token, token_type="bearer", user=current_user)
