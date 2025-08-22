"""
Reviewer Selection Pydantic schemas for data validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .user import UserResponse


class ReviewerSelectionBase(BaseModel):
    """Base reviewer selection schema with common fields."""
    
    performance_cycle_id: int
    selected_reviewers: List[int] = Field(..., min_items=1)
    comments: Optional[str] = None


class ReviewerSelectionCreate(ReviewerSelectionBase):
    """Schema for creating a new reviewer selection."""
    pass


class ReviewerSelectionUpdate(BaseModel):
    """Schema for updating reviewer selection information."""
    
    selected_reviewers: Optional[List[int]] = Field(None, min_items=1)
    comments: Optional[str] = None


class ReviewerSelectionInDB(BaseModel):
    """Schema for reviewer selection data in database."""
    
    id: int
    performance_cycle_id: int
    mentee_id: int
    status: str
    submitted_at: Optional[datetime] = None
    mentor_feedback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class ReviewerSelectionResponse(BaseModel):
    """Schema for reviewer selection response."""
    
    id: int
    performance_cycle_id: int
    mentee_id: int
    selected_reviewers: List[UserResponse]
    status: str
    submitted_at: Optional[datetime] = None
    mentor_feedback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class MentorApprovalRequest(BaseModel):
    """Schema for mentor approval request."""
    
    comments: Optional[str] = None


class MentorSendBackRequest(BaseModel):
    """Schema for mentor send back request."""
    
    feedback: str = Field(..., min_length=1)
    required_changes: List[str] = Field(..., min_items=1)
