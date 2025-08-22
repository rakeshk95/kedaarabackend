"""
User service for business logic operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.exceptions import UserNotFoundException, UserAlreadyExistsException, ValidationException


class UserService:
    """Service for user business logic operations."""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            UserResponse: User data
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return UserResponse.from_orm(user)
    
    def get_user_by_email(self, email: str) -> UserResponse:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            UserResponse: User data
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = self.repository.get_by_email(email)
        if not user:
            raise UserNotFoundException(f"User with email {email} not found")
        return UserResponse.from_orm(user)
    
    def get_users(self, skip: int = 0, limit: int = 100, role: Optional[str] = None, department: Optional[str] = None) -> List[UserResponse]:
        """
        Get all users with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            role: Filter by role
            department: Filter by department
            
        Returns:
            List[UserResponse]: List of users
        """
        users = self.repository.get_all(skip=skip, limit=limit, role=role, department=department)
        return [UserResponse.from_orm(user) for user in users]
    
    def get_available_reviewers(self, exclude_user_id: Optional[int] = None, department: Optional[str] = None) -> List[UserResponse]:
        """
        Get available reviewers (Mentors and People Committee members).
        
        Args:
            exclude_user_id: User ID to exclude from results
            department: Filter by department
            
        Returns:
            List[UserResponse]: List of available reviewers
        """
        reviewers = self.repository.get_available_reviewers(exclude_user_id=exclude_user_id, department=department)
        return [UserResponse.from_orm(reviewer) for reviewer in reviewers]
    
    def create_user(self, user_create: UserCreate) -> UserResponse:
        """
        Create a new user.
        
        Args:
            user_create: User creation data
            
        Returns:
            UserResponse: Created user data
            
        Raises:
            UserAlreadyExistsException: If user with same email already exists
            ValidationException: If validation fails
        """
        # Check if user with same email already exists
        existing_user = self.repository.get_by_email(user_create.email)
        if existing_user:
            raise UserAlreadyExistsException(f"User with email {user_create.email} already exists")
        
        # Validate password strength
        if len(user_create.password) < 8:
            raise ValidationException("Password must be at least 8 characters long")
        
        # Validate role
        valid_roles = ["Employee", "Mentor", "HR Lead", "System Administrator", "People Committee"]
        if user_create.role not in valid_roles:
            raise ValidationException(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        user = self.repository.create(user_create)
        return UserResponse.from_orm(user)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        """
        Update user information.
        
        Args:
            user_id: User ID
            user_update: User update data
            
        Returns:
            UserResponse: Updated user data
            
        Raises:
            UserNotFoundException: If user not found
            UserAlreadyExistsException: If user with same email already exists
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Check if email is being updated and if it already exists
        if user_update.email and user_update.email != user.email:
            existing_user = self.repository.get_by_email(user_update.email)
            if existing_user:
                raise UserAlreadyExistsException(f"User with email {user_update.email} already exists")
        
        # Validate role if being updated
        if user_update.role:
            valid_roles = ["Employee", "Mentor", "HR Lead", "System Administrator", "People Committee"]
            if user_update.role not in valid_roles:
                raise ValidationException(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        updated_user = self.repository.update(user_id, user_update)
        if not updated_user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        return UserResponse.from_orm(updated_user)
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        return self.repository.delete(user_id)
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Optional[UserResponse]: User data if authentication successful, None otherwise
        """
        user = self.repository.authenticate(email, password)
        if not user:
            return None
        return UserResponse.from_orm(user)
