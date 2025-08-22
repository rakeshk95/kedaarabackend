"""
Feedback Form repository for database operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.feedback_form import FeedbackForm
from app.schemas.feedback_form import FeedbackFormCreate, FeedbackFormUpdate


class FeedbackFormRepository:
    """Repository for feedback form database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, form_id: int) -> Optional[FeedbackForm]:
        """
        Get feedback form by ID.
        
        Args:
            form_id: Feedback form ID
            
        Returns:
            Optional[FeedbackForm]: Feedback form object if found, None otherwise
        """
        return self.db.query(FeedbackForm).filter(FeedbackForm.id == form_id).first()
    
    def get_by_reviewer_id(self, reviewer_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[FeedbackForm]:
        """
        Get feedback forms by reviewer ID.
        
        Args:
            reviewer_id: Reviewer user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[FeedbackForm]: List of feedback forms
        """
        query = self.db.query(FeedbackForm).filter(FeedbackForm.reviewer_id == reviewer_id)
        if status:
            query = query.filter(FeedbackForm.status == status)
        return query.offset(skip).limit(limit).all()
    
    def get_by_employee_id(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[FeedbackForm]:
        """
        Get feedback forms by employee ID.
        
        Args:
            employee_id: Employee user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[FeedbackForm]: List of feedback forms
        """
        return self.db.query(FeedbackForm).filter(FeedbackForm.employee_id == employee_id).offset(skip).limit(limit).all()
    
    def get_assigned_employees(self, reviewer_id: int) -> List[dict]:
        """
        Get assigned employees for a reviewer.
        
        Args:
            reviewer_id: Reviewer user ID
            
        Returns:
            List[dict]: List of assigned employees with assignment details
        """
        # This would need to be customized based on the reviewer assignment logic
        # For now, returning employees who have feedback forms from this reviewer
        return self.db.query(FeedbackForm).filter(FeedbackForm.reviewer_id == reviewer_id).all()
    
    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[FeedbackForm]:
        """
        Get all feedback forms with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[FeedbackForm]: List of feedback forms
        """
        query = self.db.query(FeedbackForm)
        if status:
            query = query.filter(FeedbackForm.status == status)
        return query.offset(skip).limit(limit).all()
    
    def create(self, form_create: FeedbackFormCreate, reviewer_id: int) -> FeedbackForm:
        """
        Create a new feedback form.
        
        Args:
            form_create: Feedback form creation data
            reviewer_id: Reviewer user ID
            
        Returns:
            FeedbackForm: Created feedback form object
        """
        db_form = FeedbackForm(
            employee_id=form_create.employee_id,
            reviewer_id=reviewer_id,
            performance_cycle_id=form_create.performance_cycle_id,
            strengths=form_create.strengths,
            improvements=form_create.improvements,
            overall_rating=form_create.overall_rating,
            status=form_create.status
        )
        self.db.add(db_form)
        self.db.commit()
        self.db.refresh(db_form)
        return db_form
    
    def update(self, form_id: int, form_update: FeedbackFormUpdate) -> Optional[FeedbackForm]:
        """
        Update feedback form information.
        
        Args:
            form_id: Feedback form ID
            form_update: Feedback form update data
            
        Returns:
            Optional[FeedbackForm]: Updated feedback form object if found, None otherwise
        """
        db_form = self.get_by_id(form_id)
        if not db_form:
            return None
        
        update_data = form_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_form, field, value)
        
        self.db.commit()
        self.db.refresh(db_form)
        return db_form
    
    def delete(self, form_id: int) -> bool:
        """
        Delete feedback form by ID.
        
        Args:
            form_id: Feedback form ID
            
        Returns:
            bool: True if feedback form was deleted, False if not found
        """
        db_form = self.get_by_id(form_id)
        if not db_form:
            return False
        
        self.db.delete(db_form)
        self.db.commit()
        return True
