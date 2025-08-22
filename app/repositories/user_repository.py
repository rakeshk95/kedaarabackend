"""
User repository for database operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserRepository:
    """Repository for user database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, role: Optional[str] = None, department: Optional[str] = None) -> List[User]:
        """
        Get all users with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            role: Filter by role
            department: Filter by department
            
        Returns:
            List[User]: List of users
        """
        query = self.db.query(User)
        if role:
            query = query.filter(User.role == role)
        if department:
            query = query.filter(User.department == department)
        return query.offset(skip).limit(limit).all()
    
    def get_available_reviewers(self, exclude_user_id: Optional[int] = None, department: Optional[str] = None) -> List[User]:
        """
        Get available reviewers (Mentors and People Committee members).
        
        Args:
            exclude_user_id: User ID to exclude from results
            department: Filter by department
            
        Returns:
            List[User]: List of available reviewers
        """
        query = self.db.query(User).filter(
            User.is_active == True,
            User.role.in_(["Mentor", "People Committee"])
        )
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        if department:
            query = query.filter(User.department == department)
        return query.all()
    
    def create(self, user_create: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_create: User creation data
            
        Returns:
            User: Created user object
        """
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            role=user_create.role,
            department=user_create.department,
            position=user_create.position,
            password_hash=hashed_password,
            is_active=user_create.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """
        Update user information.
        
        Args:
            user_id: User ID
            user_update: User update data
            
        Returns:
            Optional[User]: Updated user object if found, None otherwise
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        user = self.get_by_email(email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
