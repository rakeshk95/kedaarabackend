"""
Performance Cycle database model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class PerformanceCycle(Base):
    """Performance Cycle model for database representation."""
    
    __tablename__ = "performance_cycles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)  # active, inactive, completed
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.getutcdate())
    updated_at = Column(DateTime(timezone=True), onupdate=func.getutcdate())
    
    # Relationships
    reviewer_selections = relationship("ReviewerSelection", back_populates="performance_cycle")
    feedback_forms = relationship("FeedbackForm", back_populates="performance_cycle")
    
    def __repr__(self) -> str:
        return f"<PerformanceCycle(id={self.id}, name='{self.name}', status='{self.status}')>"
