"""
Feedback Form database model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class FeedbackForm(Base):
    """Feedback Form model for database representation."""
    
    __tablename__ = "feedback_forms"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    performance_cycle_id = Column(Integer, ForeignKey("performance_cycles.id"), nullable=False)
    strengths = Column(Text, nullable=False)
    improvements = Column(Text, nullable=False)
    overall_rating = Column(String(50), nullable=False)  # tracking_below, tracking_expected, tracking_above
    status = Column(String(50), nullable=False)  # draft, submitted
    created_at = Column(DateTime(timezone=True), server_default=func.getutcdate())
    updated_at = Column(DateTime(timezone=True), onupdate=func.getutcdate())
    
    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="received_feedback")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="given_feedback")
    performance_cycle = relationship("PerformanceCycle", back_populates="feedback_forms")
    
    def __repr__(self) -> str:
        return f"<FeedbackForm(id={self.id}, employee_id={self.employee_id}, reviewer_id={self.reviewer_id}, status='{self.status}')>"
