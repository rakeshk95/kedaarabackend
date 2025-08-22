"""
Notification service for business logic operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from app.utils.exceptions import NotificationNotFoundException, ValidationException


class NotificationService:
    """Service for notification business logic operations."""
    
    def __init__(self, db: Session):
        self.repository = NotificationRepository(db)
    
    def get_notification_by_id(self, notification_id: int) -> NotificationResponse:
        """
        Get notification by ID.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            NotificationResponse: Notification data
            
        Raises:
            NotificationNotFoundException: If notification not found
        """
        notification = self.repository.get_by_id(notification_id)
        if not notification:
            raise NotificationNotFoundException(f"Notification with ID {notification_id} not found")
        return NotificationResponse.from_orm(notification)
    
    def get_user_notifications(self, user_id: int, skip: int = 0, limit: int = 100, unread_only: bool = False) -> List[NotificationResponse]:
        """
        Get notifications for a user.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            unread_only: Filter to unread notifications only
            
        Returns:
            List[NotificationResponse]: List of notifications
        """
        notifications = self.repository.get_by_user_id(user_id, skip=skip, limit=limit, unread_only=unread_only)
        return [NotificationResponse.from_orm(notification) for notification in notifications]
    
    def create_notification(self, notification_create: NotificationCreate, user_id: int) -> NotificationResponse:
        """
        Create a new notification.
        
        Args:
            notification_create: Notification creation data
            user_id: User ID
            
        Returns:
            NotificationResponse: Created notification data
        """
        notification = self.repository.create(notification_create, user_id)
        return NotificationResponse.from_orm(notification)
    
    def update_notification(self, notification_id: int, notification_update: NotificationUpdate) -> NotificationResponse:
        """
        Update notification.
        
        Args:
            notification_id: Notification ID
            notification_update: Notification update data
            
        Returns:
            NotificationResponse: Updated notification data
            
        Raises:
            NotificationNotFoundException: If notification not found
        """
        notification = self.repository.update(notification_id, notification_update)
        if not notification:
            raise NotificationNotFoundException(f"Notification with ID {notification_id} not found")
        return NotificationResponse.from_orm(notification)
    
    def mark_as_read(self, notification_id: int) -> NotificationResponse:
        """
        Mark notification as read.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            NotificationResponse: Updated notification data
            
        Raises:
            NotificationNotFoundException: If notification not found
        """
        notification = self.repository.mark_as_read(notification_id)
        if not notification:
            raise NotificationNotFoundException(f"Notification with ID {notification_id} not found")
        return NotificationResponse.from_orm(notification)
    
    def mark_all_as_read(self, user_id: int) -> int:
        """
        Mark all notifications as read for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of notifications marked as read
        """
        return self.repository.mark_all_as_read(user_id)
    
    def delete_notification(self, notification_id: int) -> bool:
        """
        Delete notification by ID.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            bool: True if notification was deleted, False if not found
        """
        return self.repository.delete(notification_id)
    
    def get_unread_count(self, user_id: int) -> int:
        """
        Get count of unread notifications for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Count of unread notifications
        """
        return self.repository.get_unread_count(user_id)
    
    def get_all_notifications(self, skip: int = 0, limit: int = 100) -> List[NotificationResponse]:
        """
        Get all notifications (admin only).
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[NotificationResponse]: List of notifications
        """
        notifications = self.repository.get_all(skip=skip, limit=limit)
        return [NotificationResponse.from_orm(notification) for notification in notifications]
