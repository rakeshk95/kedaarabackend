"""
Custom exception classes for the application.
"""

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    """Exception raised when user is not found."""
    
    def __init__(self, user_id: int = None, email: str = None, username: str = None):
        detail = "User not found"
        if user_id:
            detail = f"User with ID {user_id} not found"
        elif email:
            detail = f"User with email {email} not found"
        elif username:
            detail = f"User with username {username} not found"
        
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UserAlreadyExistsException(HTTPException):
    """Exception raised when user already exists."""
    
    def __init__(self, email: str = None, username: str = None):
        detail = "User already exists"
        if email:
            detail = f"User with email {email} already exists"
        elif username:
            detail = f"User with username {username} already exists"
        
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class AuthenticationException(HTTPException):
    """Exception raised when authentication fails."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class PermissionDeniedException(HTTPException):
    """Exception raised when user doesn't have required permissions."""
    
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ValidationException(HTTPException):
    """Exception raised when data validation fails."""
    
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class PerformanceCycleNotFoundException(HTTPException):
    """Exception raised when a performance cycle is not found."""
    
    def __init__(self, detail: str = "Performance cycle not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ReviewerSelectionNotFoundException(HTTPException):
    """Exception raised when a reviewer selection is not found."""
    
    def __init__(self, detail: str = "Reviewer selection not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class FeedbackFormNotFoundException(HTTPException):
    """Exception raised when a feedback form is not found."""
    
    def __init__(self, detail: str = "Feedback form not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotificationNotFoundException(HTTPException):
    """Exception raised when a notification is not found."""
    
    def __init__(self, detail: str = "Notification not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
