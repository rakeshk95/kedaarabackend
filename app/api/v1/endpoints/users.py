"""
User management endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.dependencies import get_current_active_user, get_current_user, get_user_service
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> UserResponse:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user information
    """
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
def update_users_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Update current user information.
    
    Args:
        user_update: User update data
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        UserResponse: Updated user information
        
    Raises:
        HTTPException: If update fails
    """
    try:
        updated_user = user_service.update_user(current_user.id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    role: Optional[str] = Query(None, description="Filter by user role"),
    department: Optional[str] = Query(None, description="Filter by department"),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """
    Get all users with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        role: Filter by user role
        department: Filter by department
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        List[UserResponse]: List of users
    """
    # Only Admin and HR can access this endpoint
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    users = user_service.get_users(skip=skip, limit=limit, role=role, department=department)
    return users


@router.post("/", response_model=UserResponse)
def create_user(
    user_create: UserCreate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Create a new user (Admin/HR only).
    
    Args:
        user_create: User creation data
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        UserResponse: Created user information
        
    Raises:
        HTTPException: If user creation fails
    """
    # Only Admin and HR can create users
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    try:
        user = user_service.create_user(user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Get user by ID (Admin/HR only, or own profile).
    
    Args:
        user_id: User ID
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        UserResponse: User information
        
    Raises:
        HTTPException: If user not found or insufficient permissions
    """
    # Users can only view their own profile unless they are Admin/HR
    if current_user.id != user_id and current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Update user by ID (Admin/HR only, or own profile).
    
    Args:
        user_id: User ID
        user_update: User update data
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        UserResponse: Updated user information
        
    Raises:
        HTTPException: If update fails or insufficient permissions
    """
    # Users can only update their own profile unless they are Admin/HR
    if current_user.id != user_id and current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    try:
        updated_user = user_service.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> dict:
    """
    Delete user by ID (Admin only).
    
    Args:
        user_id: User ID
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If user not found or insufficient permissions
    """
    # Only Admin can delete users
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Prevent self-deletion
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}


@router.get("/available-reviewers", response_model=List[UserResponse])
def get_available_reviewers(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """
    Get list of available reviewers (Admin/HR/Mentor only).
    
    Args:
        current_user: Current authenticated user
        user_service: User service instance
        
    Returns:
        List[UserResponse]: List of available reviewers
    """
    # Only Admin, HR, and Mentor can access this endpoint
    if current_user.role not in ["Admin", "HR", "Mentor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    reviewers = user_service.get_available_reviewers()
    return reviewers
