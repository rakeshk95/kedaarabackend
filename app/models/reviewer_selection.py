"""
Reviewer Selection database models.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class ReviewerSelection(Base):
    """Reviewer Selection model for database representation."""
    
    __tablename__ = "reviewer_selections"
    
    id = Column(Integer, primary_key=True, index=True)
    performance_cycle_id = Column(Integer, ForeignKey("performance_cycles.id"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # pending, approved, sent_back
    submitted_at = Column(DateTime, nullable=True)
    mentor_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.getutcdate())
    updated_at = Column(DateTime(timezone=True), onupdate=func.getutcdate())
    
    # Relationships
    performance_cycle = relationship("PerformanceCycle", back_populates="reviewer_selections")
    mentee = relationship("User", foreign_keys=[mentee_id], back_populates="reviewer_selections")
    reviewer_details = relationship("ReviewerSelectionDetail", back_populates="selection", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<ReviewerSelection(id={self.id}, mentee_id={self.mentee_id}, status='{self.status}')>"


class ReviewerSelectionDetail(Base):
    """Reviewer Selection Detail model for database representation."""
    
    __tablename__ = "reviewer_selection_details"
    
    id = Column(Integer, primary_key=True, index=True)
    selection_id = Column(Integer, ForeignKey("reviewer_selections.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.getutcdate())
    
    # Relationships
    selection = relationship("ReviewerSelection", back_populates="reviewer_details")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    
    def __repr__(self) -> str:
        return f"<ReviewerSelectionDetail(id={self.id}, selection_id={self.selection_id}, reviewer_id={self.reviewer_id})>"
