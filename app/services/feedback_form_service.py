"""
Feedback Form service for business logic operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.feedback_form_repository import FeedbackFormRepository
from app.repositories.performance_cycle_repository import PerformanceCycleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.feedback_form import FeedbackFormCreate, FeedbackFormUpdate, FeedbackFormResponse
from app.utils.exceptions import (
    FeedbackFormNotFoundException, 
    ValidationException,
    PerformanceCycleNotFoundException,
    UserNotFoundException
)


class FeedbackFormService:
    """Service for feedback form business logic operations."""
    
    def __init__(self, db: Session):
        self.repository = FeedbackFormRepository(db)
        self.cycle_repository = PerformanceCycleRepository(db)
        self.user_repository = UserRepository(db)
    
    def get_form_by_id(self, form_id: int) -> FeedbackFormResponse:
        """
        Get feedback form by ID.
        
        Args:
            form_id: Feedback form ID
            
        Returns:
            FeedbackFormResponse: Feedback form data
            
        Raises:
            FeedbackFormNotFoundException: If feedback form not found
        """
        form = self.repository.get_by_id(form_id)
        if not form:
            raise FeedbackFormNotFoundException(f"Feedback form with ID {form_id} not found")
        return FeedbackFormResponse.from_orm(form)
    
    def get_forms_by_reviewer(self, reviewer_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[FeedbackFormResponse]:
        """
        Get feedback forms by reviewer ID.
        
        Args:
            reviewer_id: Reviewer user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[FeedbackFormResponse]: List of feedback forms
        """
        forms = self.repository.get_by_reviewer_id(reviewer_id, skip=skip, limit=limit, status=status)
        return [FeedbackFormResponse.from_orm(form) for form in forms]
    
    def get_forms_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[FeedbackFormResponse]:
        """
        Get feedback forms by employee ID.
        
        Args:
            employee_id: Employee user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[FeedbackFormResponse]: List of feedback forms
        """
        forms = self.repository.get_by_employee_id(employee_id, skip=skip, limit=limit)
        return [FeedbackFormResponse.from_orm(form) for form in forms]
    
    def get_assigned_employees(self, reviewer_id: int) -> List[dict]:
        """
        Get assigned employees for a reviewer.
        
        Args:
            reviewer_id: Reviewer user ID
            
        Returns:
            List[dict]: List of assigned employees with assignment details
        """
        assigned_employees = self.repository.get_assigned_employees(reviewer_id)
        result = []
        
        for assignment in assigned_employees:
            # Get employee details
            employee = self.user_repository.get_by_id(assignment.employee_id)
            if not employee:
                continue
            
            # Get performance cycle details
            cycle = self.cycle_repository.get_by_id(assignment.performance_cycle_id)
            
            assignment_data = {
                "id": assignment.id,
                "employee": {
                    "id": employee.id,
                    "name": employee.name,
                    "email": employee.email,
                    "department": employee.department,
                    "position": employee.position
                },
                "performance_cycle": {
                    "id": cycle.id,
                    "name": cycle.name
                } if cycle else None,
                "assignment_date": assignment.created_at,
                "feedback_status": assignment.status
            }
            result.append(assignment_data)
        
        return result
    
    def create_form(self, form_create: FeedbackFormCreate, reviewer_id: int) -> FeedbackFormResponse:
        """
        Create a new feedback form.
        
        Args:
            form_create: Feedback form creation data
            reviewer_id: Reviewer user ID
            
        Returns:
            FeedbackFormResponse: Created feedback form data
            
        Raises:
            ValidationException: If validation fails
            PerformanceCycleNotFoundException: If performance cycle not found
            UserNotFoundException: If employee not found
        """
        # Validate performance cycle exists and is active
        cycle = self.cycle_repository.get_by_id(form_create.performance_cycle_id)
        if not cycle:
            raise PerformanceCycleNotFoundException(f"Performance cycle with ID {form_create.performance_cycle_id} not found")
        
        if cycle.status != "active":
            raise ValidationException("Can only create feedback forms for active performance cycles")
        
        # Validate employee exists and is active
        employee = self.user_repository.get_by_id(form_create.employee_id)
        if not employee:
            raise UserNotFoundException(f"Employee with ID {form_create.employee_id} not found")
        if not employee.is_active:
            raise ValidationException(f"Employee {employee.name} is not active")
        
        # Check if reviewer already has a feedback form for this employee in this cycle
        existing_forms = self.repository.get_by_reviewer_id(reviewer_id)
        for form in existing_forms:
            if form.employee_id == form_create.employee_id and form.performance_cycle_id == form_create.performance_cycle_id:
                raise ValidationException("You already have a feedback form for this employee in this performance cycle")
        
        form = self.repository.create(form_create, reviewer_id)
        return FeedbackFormResponse.from_orm(form)
    
    def update_form(self, form_id: int, form_update: FeedbackFormUpdate, reviewer_id: int) -> FeedbackFormResponse:
        """
        Update feedback form.
        
        Args:
            form_id: Feedback form ID
            form_update: Feedback form update data
            reviewer_id: Reviewer user ID (for authorization)
            
        Returns:
            FeedbackFormResponse: Updated feedback form data
            
        Raises:
            FeedbackFormNotFoundException: If feedback form not found
            ValidationException: If validation fails
        """
        form = self.repository.get_by_id(form_id)
        if not form:
            raise FeedbackFormNotFoundException(f"Feedback form with ID {form_id} not found")
        
        # Check authorization
        if form.reviewer_id != reviewer_id:
            raise ValidationException("You can only update your own feedback forms")
        
        # Check if form can be updated
        if form.status == "submitted":
            raise ValidationException("Cannot update submitted feedback forms")
        
        updated_form = self.repository.update(form_id, form_update)
        if not updated_form:
            raise FeedbackFormNotFoundException(f"Feedback form with ID {form_id} not found")
        
        return FeedbackFormResponse.from_orm(updated_form)
    
    def delete_form(self, form_id: int, reviewer_id: int) -> bool:
        """
        Delete feedback form.
        
        Args:
            form_id: Feedback form ID
            reviewer_id: Reviewer user ID (for authorization)
            
        Returns:
            bool: True if feedback form was deleted, False if not found
            
        Raises:
            ValidationException: If user is not authorized to delete the form
        """
        form = self.repository.get_by_id(form_id)
        if not form:
            return False
        
        # Check authorization
        if form.reviewer_id != reviewer_id:
            raise ValidationException("You can only delete your own feedback forms")
        
        # Check if form can be deleted
        if form.status == "submitted":
            raise ValidationException("Cannot delete submitted feedback forms")
        
        return self.repository.delete(form_id)
    
    def get_all_forms(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[FeedbackFormResponse]:
        """
        Get all feedback forms with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[FeedbackFormResponse]: List of feedback forms
        """
        forms = self.repository.get_all(skip=skip, limit=limit, status=status)
        return [FeedbackFormResponse.from_orm(form) for form in forms]
