"""
Feedback Form Pydantic schemas for data validation and serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FeedbackFormBase(BaseModel):
    """Base feedback form schema with common fields."""
    
    employee_id: int
    performance_cycle_id: int
    strengths: str = Field(..., min_length=1)
    improvements: str = Field(..., min_length=1)
    overall_rating: str = Field(..., pattern="^(tracking_below|tracking_expected|tracking_above)$")
    status: str = Field(..., pattern="^(draft|submitted)$")


class FeedbackFormCreate(FeedbackFormBase):
    """Schema for creating a new feedback form."""
    pass


class FeedbackFormUpdate(BaseModel):
    """Schema for updating feedback form information."""
    
    strengths: Optional[str] = Field(None, min_length=1)
    improvements: Optional[str] = Field(None, min_length=1)
    overall_rating: Optional[str] = Field(None, pattern="^(tracking_below|tracking_expected|tracking_above)$")
    status: Optional[str] = Field(None, pattern="^(draft|submitted)$")


class FeedbackFormInDB(FeedbackFormBase):
    """Schema for feedback form data in database."""
    
    id: int
    reviewer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class FeedbackFormResponse(FeedbackFormBase):
    """Schema for feedback form response."""
    
    id: int
    reviewer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }
