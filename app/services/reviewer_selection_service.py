"""
Reviewer Selection service for business logic operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.reviewer_selection_repository import ReviewerSelectionRepository
from app.repositories.performance_cycle_repository import PerformanceCycleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.reviewer_selection import (
    ReviewerSelectionCreate, 
    ReviewerSelectionUpdate, 
    ReviewerSelectionResponse,
    MentorApprovalRequest,
    MentorSendBackRequest
)
from app.schemas.user import UserResponse
from app.utils.exceptions import (
    ReviewerSelectionNotFoundException, 
    ValidationException,
    PerformanceCycleNotFoundException,
    UserNotFoundException
)


class ReviewerSelectionService:
    """Service for reviewer selection business logic operations."""
    
    def __init__(self, db: Session):
        self.repository = ReviewerSelectionRepository(db)
        self.cycle_repository = PerformanceCycleRepository(db)
        self.user_repository = UserRepository(db)
    
    def get_my_selection(self, mentee_id: int, cycle_id: Optional[int] = None) -> Optional[ReviewerSelectionResponse]:
        """
        Get current user's reviewer selection.
        
        Args:
            mentee_id: Mentee user ID
            cycle_id: Optional performance cycle ID
            
        Returns:
            Optional[ReviewerSelectionResponse]: Reviewer selection data if found, None otherwise
        """
        selection = self.repository.get_by_mentee_id(mentee_id, cycle_id)
        if not selection:
            return None
        
        # Get selected reviewers
        selected_reviewers = self.repository.get_selected_reviewers(selection.id)
        reviewer_responses = [UserResponse.from_orm(reviewer) for reviewer in selected_reviewers]
        
        # Create response with selected reviewers
        response_data = ReviewerSelectionResponse.from_orm(selection)
        response_data.selected_reviewers = reviewer_responses
        return response_data
    
    def create_selection(self, selection_create: ReviewerSelectionCreate, mentee_id: int) -> ReviewerSelectionResponse:
        """
        Create a new reviewer selection.
        
        Args:
            selection_create: Reviewer selection creation data
            mentee_id: Mentee user ID
            
        Returns:
            ReviewerSelectionResponse: Created reviewer selection data
            
        Raises:
            ValidationException: If validation fails
            PerformanceCycleNotFoundException: If performance cycle not found
            UserNotFoundException: If any reviewer not found
        """
        # Validate performance cycle exists and is active
        cycle = self.cycle_repository.get_by_id(selection_create.performance_cycle_id)
        if not cycle:
            raise PerformanceCycleNotFoundException(f"Performance cycle with ID {selection_create.performance_cycle_id} not found")
        
        if cycle.status != "active":
            raise ValidationException("Can only submit reviewer selections for active performance cycles")
        
        # Validate all reviewers exist and are available
        for reviewer_id in selection_create.selected_reviewers:
            reviewer = self.user_repository.get_by_id(reviewer_id)
            if not reviewer:
                raise UserNotFoundException(f"Reviewer with ID {reviewer_id} not found")
            if not reviewer.is_active:
                raise ValidationException(f"Reviewer {reviewer.name} is not active")
            if reviewer.role not in ["Mentor", "People Committee"]:
                raise ValidationException(f"User {reviewer.name} is not eligible as a reviewer")
        
        # Check if user already has a selection for this cycle
        existing_selection = self.repository.get_by_mentee_id(mentee_id, selection_create.performance_cycle_id)
        if existing_selection:
            raise ValidationException("You already have a reviewer selection for this performance cycle")
        
        selection = self.repository.create(selection_create, mentee_id)
        
        # Get selected reviewers for response
        selected_reviewers = self.repository.get_selected_reviewers(selection.id)
        reviewer_responses = [UserResponse.from_orm(reviewer) for reviewer in selected_reviewers]
        
        # Create response with selected reviewers
        response_data = ReviewerSelectionResponse.from_orm(selection)
        response_data.selected_reviewers = reviewer_responses
        return response_data
    
    def update_selection(self, selection_id: int, selection_update: ReviewerSelectionUpdate, mentee_id: int) -> ReviewerSelectionResponse:
        """
        Update reviewer selection.
        
        Args:
            selection_id: Reviewer selection ID
            selection_update: Reviewer selection update data
            mentee_id: Mentee user ID (for authorization)
            
        Returns:
            ReviewerSelectionResponse: Updated reviewer selection data
            
        Raises:
            ReviewerSelectionNotFoundException: If reviewer selection not found
            ValidationException: If validation fails
            UserNotFoundException: If any reviewer not found
        """
        selection = self.repository.get_by_id(selection_id)
        if not selection:
            raise ReviewerSelectionNotFoundException(f"Reviewer selection with ID {selection_id} not found")
        
        # Check authorization
        if selection.mentee_id != mentee_id:
            raise ValidationException("You can only update your own reviewer selection")
        
        # Check if selection can be updated
        if selection.status != "pending" and selection.status != "sent_back":
            raise ValidationException("Can only update pending or sent back selections")
        
        # Validate reviewers if provided
        if selection_update.selected_reviewers:
            for reviewer_id in selection_update.selected_reviewers:
                reviewer = self.user_repository.get_by_id(reviewer_id)
                if not reviewer:
                    raise UserNotFoundException(f"Reviewer with ID {reviewer_id} not found")
                if not reviewer.is_active:
                    raise ValidationException(f"Reviewer {reviewer.name} is not active")
                if reviewer.role not in ["Mentor", "People Committee"]:
                    raise ValidationException(f"User {reviewer.name} is not eligible as a reviewer")
        
        updated_selection = self.repository.update(selection_id, selection_update)
        if not updated_selection:
            raise ReviewerSelectionNotFoundException(f"Reviewer selection with ID {selection_id} not found")
        
        # Get selected reviewers for response
        selected_reviewers = self.repository.get_selected_reviewers(updated_selection.id)
        reviewer_responses = [UserResponse.from_orm(reviewer) for reviewer in selected_reviewers]
        
        # Create response with selected reviewers
        response_data = ReviewerSelectionResponse.from_orm(updated_selection)
        response_data.selected_reviewers = reviewer_responses
        return response_data
    
    def get_pending_approvals(self, mentor_id: int) -> List[dict]:
        """
        Get pending approvals for a mentor.
        
        Args:
            mentor_id: Mentor user ID
            
        Returns:
            List[dict]: List of pending approvals with details
        """
        pending_selections = self.repository.get_pending_approvals(mentor_id)
        approvals = []
        
        for selection in pending_selections:
            # Get mentee details
            mentee = self.user_repository.get_by_id(selection.mentee_id)
            if not mentee:
                continue
            
            # Get selected reviewers
            selected_reviewers = self.repository.get_selected_reviewers(selection.id)
            reviewer_responses = [UserResponse.from_orm(reviewer) for reviewer in selected_reviewers]
            
            # Get performance cycle details
            cycle = self.cycle_repository.get_by_id(selection.performance_cycle_id)
            
            approval_data = {
                "id": selection.id,
                "mentee": UserResponse.from_orm(mentee),
                "selected_reviewers": reviewer_responses,
                "status": selection.status,
                "submitted_at": selection.submitted_at,
                "performance_cycle": {
                    "id": cycle.id,
                    "name": cycle.name
                } if cycle else None
            }
            approvals.append(approval_data)
        
        return approvals
    
    def approve_selection(self, selection_id: int, approval_request: MentorApprovalRequest) -> ReviewerSelectionResponse:
        """
        Approve a reviewer selection.
        
        Args:
            selection_id: Reviewer selection ID
            approval_request: Approval request data
            
        Returns:
            ReviewerSelectionResponse: Updated reviewer selection data
            
        Raises:
            ReviewerSelectionNotFoundException: If reviewer selection not found
            ValidationException: If validation fails
        """
        selection = self.repository.get_by_id(selection_id)
        if not selection:
            raise ReviewerSelectionNotFoundException(f"Reviewer selection with ID {selection_id} not found")
        
        if selection.status != "pending":
            raise ValidationException("Can only approve pending selections")
        
        approved_selection = self.repository.approve(selection_id, approval_request.comments)
        if not approved_selection:
            raise ReviewerSelectionNotFoundException(f"Reviewer selection with ID {selection_id} not found")
        
        # Get selected reviewers for response
        selected_reviewers = self.repository.get_selected_reviewers(approved_selection.id)
        reviewer_responses = [UserResponse.from_orm(reviewer) for reviewer in selected_reviewers]
        
        # Create response with selected reviewers
        response_data = ReviewerSelectionResponse.from_orm(approved_selection)
        response_data.selected_reviewers = reviewer_responses
        return response_data
    
    def send_back_selection(self, selection_id: int, send_back_request: MentorSendBackRequest) -> ReviewerSelectionResponse:
        """
        Send back a reviewer selection for revision.
        
        Args:
            selection_id: Reviewer selection ID
            send_back_request: Send back request data
            
        Returns:
            ReviewerSelectionResponse: Updated reviewer selection data
            
        Raises:
            ReviewerSelectionNotFoundException: If reviewer selection not found
            ValidationException: If validation fails
        """
        selection = self.repository.get_by_id(selection_id)
        if not selection:
            raise ReviewerSelectionNotFoundException(f"Reviewer selection with ID {selection_id} not found")
        
        if selection.status != "pending":
            raise ValidationException("Can only send back pending selections")
        
        sent_back_selection = self.repository.send_back(selection_id, send_back_request.feedback)
        if not sent_back_selection:
            raise ReviewerSelectionNotFoundException(f"Reviewer selection with ID {selection_id} not found")
        
        # Get selected reviewers for response
        selected_reviewers = self.repository.get_selected_reviewers(sent_back_selection.id)
        reviewer_responses = [UserResponse.from_orm(reviewer) for reviewer in selected_reviewers]
        
        # Create response with selected reviewers
        response_data = ReviewerSelectionResponse.from_orm(sent_back_selection)
        response_data.selected_reviewers = reviewer_responses
        return response_data
    
    def delete_selection(self, selection_id: int, mentee_id: int) -> bool:
        """
        Delete reviewer selection.
        
        Args:
            selection_id: Reviewer selection ID
            mentee_id: Mentee user ID (for authorization)
            
        Returns:
            bool: True if reviewer selection was deleted, False if not found
            
        Raises:
            ValidationException: If user is not authorized to delete the selection
        """
        selection = self.repository.get_by_id(selection_id)
        if not selection:
            return False
        
        # Check authorization
        if selection.mentee_id != mentee_id:
            raise ValidationException("You can only delete your own reviewer selection")
        
        # Check if selection can be deleted
        if selection.status != "pending":
            raise ValidationException("Can only delete pending selections")
        
        return self.repository.delete(selection_id)
