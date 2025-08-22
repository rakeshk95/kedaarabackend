"""
Performance Cycle Pydantic schemas for data validation and serialization.
"""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class PerformanceCycleBase(BaseModel):
    """Base performance cycle schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: date
    status: str = Field(..., pattern="^(active|inactive|completed)$")
    description: Optional[str] = None


class PerformanceCycleCreate(PerformanceCycleBase):
    """Schema for creating a new performance cycle."""
    pass


class PerformanceCycleUpdate(BaseModel):
    """Schema for updating performance cycle information."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive|completed)$")
    description: Optional[str] = None


class PerformanceCycleInDB(PerformanceCycleBase):
    """Schema for performance cycle data in database."""
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class PerformanceCycleResponse(PerformanceCycleBase):
    """Schema for performance cycle response."""
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }
