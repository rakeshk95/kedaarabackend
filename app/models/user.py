"""
User database model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class User(Base):
    """User model for database representation."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # Employee, Mentor, HR Lead, System Administrator, People Committee
    department = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.getutcdate())
    updated_at = Column(DateTime(timezone=True), onupdate=func.getutcdate())
    
    # Relationships
    reviewer_selections = relationship("ReviewerSelection", back_populates="mentee")
    received_feedback = relationship("FeedbackForm", foreign_keys="FeedbackForm.employee_id", back_populates="employee")
    given_feedback = relationship("FeedbackForm", foreign_keys="FeedbackForm.reviewer_id", back_populates="reviewer")
    notifications = relationship("Notification", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}', role='{self.role}')>"
