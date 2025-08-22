"""
Notification repository for database operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


class NotificationRepository:
    """Repository for notification database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        Get notification by ID.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Optional[Notification]: Notification object if found, None otherwise
        """
        return self.db.query(Notification).filter(Notification.id == notification_id).first()
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100, unread_only: bool = False) -> List[Notification]:
        """
        Get notifications by user ID.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            unread_only: Filter to unread notifications only
            
        Returns:
            List[Notification]: List of notifications
        """
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Notification]:
        """
        Get all notifications.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Notification]: List of notifications
        """
        return self.db.query(Notification).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def create(self, notification_create: NotificationCreate, user_id: int) -> Notification:
        """
        Create a new notification.
        
        Args:
            notification_create: Notification creation data
            user_id: User ID
            
        Returns:
            Notification: Created notification object
        """
        db_notification = Notification(
            user_id=user_id,
            title=notification_create.title,
            message=notification_create.message,
            type=notification_create.type
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification
    
    def update(self, notification_id: int, notification_update: NotificationUpdate) -> Optional[Notification]:
        """
        Update notification information.
        
        Args:
            notification_id: Notification ID
            notification_update: Notification update data
            
        Returns:
            Optional[Notification]: Updated notification object if found, None otherwise
        """
        db_notification = self.get_by_id(notification_id)
        if not db_notification:
            return None
        
        update_data = notification_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notification, field, value)
        
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification
    
    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """
        Mark notification as read.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Optional[Notification]: Updated notification object if found, None otherwise
        """
        db_notification = self.get_by_id(notification_id)
        if not db_notification:
            return None
        
        db_notification.is_read = True
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification
    
    def mark_all_as_read(self, user_id: int) -> int:
        """
        Mark all notifications as read for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of notifications marked as read
        """
        result = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})
        self.db.commit()
        return result
    
    def delete(self, notification_id: int) -> bool:
        """
        Delete notification by ID.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            bool: True if notification was deleted, False if not found
        """
        db_notification = self.get_by_id(notification_id)
        if not db_notification:
            return False
        
        self.db.delete(db_notification)
        self.db.commit()
        return True
    
    def get_unread_count(self, user_id: int) -> int:
        """
        Get count of unread notifications for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Count of unread notifications
        """
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
