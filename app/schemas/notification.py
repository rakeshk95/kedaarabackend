"""
Notification Pydantic schemas for data validation and serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    """Base notification schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1, max_length=50)


class NotificationCreate(NotificationBase):
    """Schema for creating a new notification."""
    pass


class NotificationUpdate(BaseModel):
    """Schema for updating notification information."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    is_read: Optional[bool] = None


class NotificationInDB(NotificationBase):
    """Schema for notification data in database."""
    
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
