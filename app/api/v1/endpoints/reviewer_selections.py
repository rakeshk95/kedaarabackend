"""
Reviewer Selection API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.reviewer_selection_service import ReviewerSelectionService
from app.schemas.reviewer_selection import (
    ReviewerSelectionCreate,
    ReviewerSelectionUpdate,
    ReviewerSelectionResponse,
    MentorApprovalRequest,
    MentorSendBackRequest
)
from app.api.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=ReviewerSelectionResponse)
def submit_reviewer_selection(
    selection_create: ReviewerSelectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReviewerSelectionResponse:
    """
    Submit reviewer selection (Employee only).
    
    Args:
        selection_create: Reviewer selection creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ReviewerSelectionResponse: Created reviewer selection data
    """
    # Only employees can submit reviewer selections
    if current_user.role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can submit reviewer selections"
        )
    
    selection_service = ReviewerSelectionService(db)
    selection = selection_service.create_selection(selection_create, current_user.id)
    
    logger.info("Reviewer selection submitted", selection_id=selection.id, user_id=current_user.id)
    
    return selection


@router.get("/my-selection", response_model=ReviewerSelectionResponse)
def get_my_reviewer_selection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReviewerSelectionResponse:
    """
    Get current user's reviewer selection (Employee only).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ReviewerSelectionResponse: Reviewer selection data
        
    Raises:
        HTTPException: If no selection found
    """
    # Only employees can view their own selections
    if current_user.role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can view their reviewer selections"
        )
    
    selection_service = ReviewerSelectionService(db)
    selection = selection_service.get_my_selection(current_user.id)
    
    if not selection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reviewer selection found for current user"
        )
    
    return selection


@router.put("/{selection_id}", response_model=ReviewerSelectionResponse)
def update_reviewer_selection(
    selection_id: int,
    selection_update: ReviewerSelectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReviewerSelectionResponse:
    """
    Update reviewer selection (Employee only).
    
    Args:
        selection_id: Reviewer selection ID
        selection_update: Reviewer selection update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ReviewerSelectionResponse: Updated reviewer selection data
    """
    # Only employees can update their own selections
    if current_user.role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can update reviewer selections"
        )
    
    selection_service = ReviewerSelectionService(db)
    selection = selection_service.update_selection(selection_id, selection_update, current_user.id)
    
    logger.info("Reviewer selection updated", selection_id=selection_id, user_id=current_user.id)
    
    return selection


@router.delete("/{selection_id}")
def delete_reviewer_selection(
    selection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete reviewer selection (Employee only).
    
    Args:
        selection_id: Reviewer selection ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    # Only employees can delete their own selections
    if current_user.role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can delete reviewer selections"
        )
    
    selection_service = ReviewerSelectionService(db)
    success = selection_service.delete_selection(selection_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reviewer selection not found"
        )
    
    logger.info("Reviewer selection deleted", selection_id=selection_id, user_id=current_user.id)
    
    return {"message": "Reviewer selection deleted successfully"}


# Mentor endpoints
@router.get("/mentor/approvals/pending")
def get_pending_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get pending approvals for mentor.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of pending approvals
    """
    # Only mentors can view pending approvals
    if current_user.role != "Mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can view pending approvals"
        )
    
    selection_service = ReviewerSelectionService(db)
    approvals = selection_service.get_pending_approvals(current_user.id)
    
    return approvals


@router.get("/mentor/approvals")
def get_all_approvals(
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all approvals for mentor.
    
    Args:
        status: Filter by status
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of approvals
    """
    # Only mentors can view approvals
    if current_user.role != "Mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can view approvals"
        )
    
    # For now, return all pending approvals (can be enhanced with filtering)
    selection_service = ReviewerSelectionService(db)
    approvals = selection_service.get_pending_approvals(current_user.id)
    
    return approvals


@router.post("/mentor/approvals/{selection_id}/approve", response_model=ReviewerSelectionResponse)
def approve_reviewer_selection(
    selection_id: int,
    approval_request: MentorApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReviewerSelectionResponse:
    """
    Approve reviewer selection (Mentor only).
    
    Args:
        selection_id: Reviewer selection ID
        approval_request: Approval request data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ReviewerSelectionResponse: Updated reviewer selection data
    """
    # Only mentors can approve selections
    if current_user.role != "Mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can approve reviewer selections"
        )
    
    selection_service = ReviewerSelectionService(db)
    selection = selection_service.approve_selection(selection_id, approval_request)
    
    logger.info("Reviewer selection approved", selection_id=selection_id, mentor_id=current_user.id)
    
    return selection


@router.post("/mentor/approvals/{selection_id}/send-back", response_model=ReviewerSelectionResponse)
def send_back_reviewer_selection(
    selection_id: int,
    send_back_request: MentorSendBackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReviewerSelectionResponse:
    """
    Send back reviewer selection for revision (Mentor only).
    
    Args:
        selection_id: Reviewer selection ID
        send_back_request: Send back request data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ReviewerSelectionResponse: Updated reviewer selection data
    """
    # Only mentors can send back selections
    if current_user.role != "Mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can send back reviewer selections"
        )
    
    selection_service = ReviewerSelectionService(db)
    selection = selection_service.send_back_selection(selection_id, send_back_request)
    
    logger.info("Reviewer selection sent back", selection_id=selection_id, mentor_id=current_user.id)
    
    return selection


@router.get("/mentor/approvals/{selection_id}")
def get_approval_details(
    selection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get approval details (Mentor only).
    
    Args:
        selection_id: Reviewer selection ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Approval details
    """
    # Only mentors can view approval details
    if current_user.role != "Mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can view approval details"
        )
    
    selection_service = ReviewerSelectionService(db)
    approvals = selection_service.get_pending_approvals(current_user.id)
    
    # Find the specific approval
    for approval in approvals:
        if approval["id"] == selection_id:
            return approval
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Approval not found"
    )
