"""
Feedback Form API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.feedback_form_service import FeedbackFormService
from app.schemas.feedback_form import (
    FeedbackFormCreate,
    FeedbackFormUpdate,
    FeedbackFormResponse
)
from app.api.dependencies import get_current_user, get_current_superuser
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/reviewer/assignments")
def get_assigned_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get assigned employees for reviewer.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of assigned employees
    """
    # Only reviewers can view assigned employees
    if current_user.role not in ["Mentor", "People Committee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only reviewers can view assigned employees"
        )
    
    form_service = FeedbackFormService(db)
    assignments = form_service.get_assigned_employees(current_user.id)
    
    return assignments


@router.get("/reviewer/feedback-forms", response_model=List[FeedbackFormResponse])
def get_feedback_forms(
    status: Optional[str] = Query(None, description="Filter by status"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[FeedbackFormResponse]:
    """
    Get feedback forms for reviewer.
    
    Args:
        status: Filter by status
        employee_id: Filter by employee ID
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[FeedbackFormResponse]: List of feedback forms
    """
    # Only reviewers can view feedback forms
    if current_user.role not in ["Mentor", "People Committee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only reviewers can view feedback forms"
        )
    
    skip = (page - 1) * limit
    form_service = FeedbackFormService(db)
    forms = form_service.get_forms_by_reviewer(
        current_user.id, skip=skip, limit=limit, status=status
    )
    
    # Filter by employee_id if provided
    if employee_id:
        forms = [form for form in forms if form.employee_id == employee_id]
    
    return forms


@router.post("/reviewer/feedback-forms", response_model=FeedbackFormResponse)
def create_feedback_form(
    form_create: FeedbackFormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FeedbackFormResponse:
    """
    Create feedback form (Reviewer only).
    
    Args:
        form_create: Feedback form creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        FeedbackFormResponse: Created feedback form data
    """
    # Only reviewers can create feedback forms
    if current_user.role not in ["Mentor", "People Committee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only reviewers can create feedback forms"
        )
    
    form_service = FeedbackFormService(db)
    form = form_service.create_form(form_create, current_user.id)
    
    logger.info("Feedback form created", form_id=form.id, reviewer_id=current_user.id)
    
    return form


@router.get("/reviewer/feedback-forms/{form_id}", response_model=FeedbackFormResponse)
def get_feedback_form(
    form_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FeedbackFormResponse:
    """
    Get feedback form by ID (Reviewer only).
    
    Args:
        form_id: Feedback form ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        FeedbackFormResponse: Feedback form data
    """
    # Only reviewers can view feedback forms
    if current_user.role not in ["Mentor", "People Committee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only reviewers can view feedback forms"
        )
    
    form_service = FeedbackFormService(db)
    form = form_service.get_form_by_id(form_id)
    
    # Check if the form belongs to the current user
    if form.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own feedback forms"
        )
    
    return form


@router.put("/reviewer/feedback-forms/{form_id}", response_model=FeedbackFormResponse)
def update_feedback_form(
    form_id: int,
    form_update: FeedbackFormUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FeedbackFormResponse:
    """
    Update feedback form (Reviewer only).
    
    Args:
        form_id: Feedback form ID
        form_update: Feedback form update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        FeedbackFormResponse: Updated feedback form data
    """
    # Only reviewers can update feedback forms
    if current_user.role not in ["Mentor", "People Committee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only reviewers can update feedback forms"
        )
    
    form_service = FeedbackFormService(db)
    form = form_service.update_form(form_id, form_update, current_user.id)
    
    logger.info("Feedback form updated", form_id=form_id, reviewer_id=current_user.id)
    
    return form


@router.delete("/reviewer/feedback-forms/{form_id}")
def delete_feedback_form(
    form_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete feedback form (Reviewer only).
    
    Args:
        form_id: Feedback form ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    # Only reviewers can delete feedback forms
    if current_user.role not in ["Mentor", "People Committee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only reviewers can delete feedback forms"
        )
    
    form_service = FeedbackFormService(db)
    success = form_service.delete_form(form_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback form not found"
        )
    
    logger.info("Feedback form deleted", form_id=form_id, reviewer_id=current_user.id)
    
    return {"message": "Feedback form deleted successfully"}


# Employee endpoints
@router.get("/employee/feedback-forms", response_model=List[FeedbackFormResponse])
def get_my_feedback_forms(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[FeedbackFormResponse]:
    """
    Get feedback forms for current employee.
    
    Args:
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[FeedbackFormResponse]: List of feedback forms
    """
    # Only employees can view their own feedback forms
    if current_user.role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can view their feedback forms"
        )
    
    skip = (page - 1) * limit
    form_service = FeedbackFormService(db)
    forms = form_service.get_forms_by_employee(current_user.id, skip=skip, limit=limit)
    
    return forms


# Admin endpoints
@router.get("/admin/feedback-forms", response_model=List[FeedbackFormResponse])
def get_all_feedback_forms(
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> List[FeedbackFormResponse]:
    """
    Get all feedback forms (Admin/HR only).
    
    Args:
        status: Filter by status
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[FeedbackFormResponse]: List of feedback forms
    """
    skip = (page - 1) * limit
    form_service = FeedbackFormService(db)
    forms = form_service.get_all_forms(skip=skip, limit=limit, status=status)
    
    return forms
