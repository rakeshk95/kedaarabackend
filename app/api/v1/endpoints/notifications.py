"""
Notification API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse
)
from app.api.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
def get_user_notifications(
    unread_only: bool = Query(False, description="Get only unread notifications"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[NotificationResponse]:
    """
    Get notifications for current user.
    
    Args:
        unread_only: Get only unread notifications
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[NotificationResponse]: List of notifications
    """
    skip = (page - 1) * limit
    notification_service = NotificationService(db)
    notifications = notification_service.get_user_notifications(
        current_user.id, skip=skip, limit=limit, unread_only=unread_only
    )
    
    return notifications


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> NotificationResponse:
    """
    Mark notification as read.
    
    Args:
        notification_id: Notification ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Updated notification data
    """
    notification_service = NotificationService(db)
    notification = notification_service.mark_as_read(notification_id)
    
    # Check if the notification belongs to the current user
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark your own notifications as read"
        )
    
    logger.info("Notification marked as read", notification_id=notification_id, user_id=current_user.id)
    
    return notification


@router.put("/read-all")
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark all notifications as read for current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message with count
    """
    notification_service = NotificationService(db)
    count = notification_service.mark_all_as_read(current_user.id)
    
    logger.info("All notifications marked as read", user_id=current_user.id, count=count)
    
    return {"message": f"Marked {count} notifications as read"}


# Admin endpoints
@router.get("/admin/notifications", response_model=List[NotificationResponse])
def get_all_notifications(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> List[NotificationResponse]:
    """
    Get all notifications (Admin/HR only).
    
    Args:
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[NotificationResponse]: List of notifications
    """
    skip = (page - 1) * limit
    notification_service = NotificationService(db)
    notifications = notification_service.get_all_notifications(skip=skip, limit=limit)
    
    return notifications


@router.post("/admin/notifications", response_model=NotificationResponse)
def create_notification(
    notification_create: NotificationCreate,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> NotificationResponse:
    """
    Create notification for a user (Admin/HR only).
    
    Args:
        notification_create: Notification creation data
        user_id: User ID to create notification for
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Created notification data
    """
    notification_service = NotificationService(db)
    notification = notification_service.create_notification(notification_create, user_id)
    
    logger.info("Notification created", notification_id=notification.id, user_id=user_id, created_by=current_user.id)
    
    return notification


@router.put("/admin/notifications/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
) -> NotificationResponse:
    """
    Update notification (Admin/HR only).
    
    Args:
        notification_id: Notification ID
        notification_update: Notification update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Updated notification data
    """
    notification_service = NotificationService(db)
    notification = notification_service.update_notification(notification_id, notification_update)
    
    logger.info("Notification updated", notification_id=notification_id, updated_by=current_user.id)
    
    return notification


@router.delete("/admin/notifications/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Delete notification (Admin/HR only).
    
    Args:
        notification_id: Notification ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    notification_service = NotificationService(db)
    success = notification_service.delete_notification(notification_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    logger.info("Notification deleted", notification_id=notification_id, deleted_by=current_user.id)
    
    return {"message": "Notification deleted successfully"}
