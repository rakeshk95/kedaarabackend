"""
Reviewer Selection repository for database operations.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.reviewer_selection import ReviewerSelection, ReviewerSelectionDetail
from app.models.user import User
from app.schemas.reviewer_selection import ReviewerSelectionCreate, ReviewerSelectionUpdate


class ReviewerSelectionRepository:
    """Repository for reviewer selection database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, selection_id: int) -> Optional[ReviewerSelection]:
        """
        Get reviewer selection by ID.
        
        Args:
            selection_id: Reviewer selection ID
            
        Returns:
            Optional[ReviewerSelection]: Reviewer selection object if found, None otherwise
        """
        return self.db.query(ReviewerSelection).filter(ReviewerSelection.id == selection_id).first()
    
    def get_by_mentee_id(self, mentee_id: int, cycle_id: Optional[int] = None) -> Optional[ReviewerSelection]:
        """
        Get reviewer selection by mentee ID and optionally cycle ID.
        
        Args:
            mentee_id: Mentee user ID
            cycle_id: Optional performance cycle ID
            
        Returns:
            Optional[ReviewerSelection]: Reviewer selection object if found, None otherwise
        """
        query = self.db.query(ReviewerSelection).filter(ReviewerSelection.mentee_id == mentee_id)
        if cycle_id:
            query = query.filter(ReviewerSelection.performance_cycle_id == cycle_id)
        return query.first()
    
    def get_pending_approvals(self, mentor_id: int) -> List[ReviewerSelection]:
        """
        Get pending approvals for a mentor.
        
        Args:
            mentor_id: Mentor user ID
            
        Returns:
            List[ReviewerSelection]: List of pending reviewer selections
        """
        # Note: This would need to be customized based on mentor-mentee relationship logic
        return self.db.query(ReviewerSelection).filter(ReviewerSelection.status == "pending").all()
    
    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[ReviewerSelection]:
        """
        Get all reviewer selections with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[ReviewerSelection]: List of reviewer selections
        """
        query = self.db.query(ReviewerSelection)
        if status:
            query = query.filter(ReviewerSelection.status == status)
        return query.offset(skip).limit(limit).all()
    
    def create(self, selection_create: ReviewerSelectionCreate, mentee_id: int) -> ReviewerSelection:
        """
        Create a new reviewer selection.
        
        Args:
            selection_create: Reviewer selection creation data
            mentee_id: Mentee user ID
            
        Returns:
            ReviewerSelection: Created reviewer selection object
        """
        # Create the main selection record
        db_selection = ReviewerSelection(
            performance_cycle_id=selection_create.performance_cycle_id,
            mentee_id=mentee_id,
            status="pending",
            submitted_at=datetime.utcnow()
        )
        self.db.add(db_selection)
        self.db.flush()  # Get the ID without committing
        
        # Create reviewer detail records
        for reviewer_id in selection_create.selected_reviewers:
            detail = ReviewerSelectionDetail(
                selection_id=db_selection.id,
                reviewer_id=reviewer_id
            )
            self.db.add(detail)
        
        self.db.commit()
        self.db.refresh(db_selection)
        return db_selection
    
    def update(self, selection_id: int, selection_update: ReviewerSelectionUpdate) -> Optional[ReviewerSelection]:
        """
        Update reviewer selection information.
        
        Args:
            selection_id: Reviewer selection ID
            selection_update: Reviewer selection update data
            
        Returns:
            Optional[ReviewerSelection]: Updated reviewer selection object if found, None otherwise
        """
        db_selection = self.get_by_id(selection_id)
        if not db_selection:
            return None
        
        update_data = selection_update.dict(exclude_unset=True)
        
        # Handle selected_reviewers separately
        if "selected_reviewers" in update_data:
            # Delete existing reviewer details
            self.db.query(ReviewerSelectionDetail).filter(
                ReviewerSelectionDetail.selection_id == selection_id
            ).delete()
            
            # Create new reviewer details
            for reviewer_id in update_data["selected_reviewers"]:
                detail = ReviewerSelectionDetail(
                    selection_id=selection_id,
                    reviewer_id=reviewer_id
                )
                self.db.add(detail)
            
            del update_data["selected_reviewers"]
        
        # Update other fields
        for field, value in update_data.items():
            setattr(db_selection, field, value)
        
        self.db.commit()
        self.db.refresh(db_selection)
        return db_selection
    
    def approve(self, selection_id: int, mentor_feedback: Optional[str] = None) -> Optional[ReviewerSelection]:
        """
        Approve a reviewer selection.
        
        Args:
            selection_id: Reviewer selection ID
            mentor_feedback: Optional mentor feedback
            
        Returns:
            Optional[ReviewerSelection]: Updated reviewer selection object if found, None otherwise
        """
        db_selection = self.get_by_id(selection_id)
        if not db_selection:
            return None
        
        db_selection.status = "approved"
        db_selection.mentor_feedback = mentor_feedback
        
        self.db.commit()
        self.db.refresh(db_selection)
        return db_selection
    
    def send_back(self, selection_id: int, mentor_feedback: str) -> Optional[ReviewerSelection]:
        """
        Send back a reviewer selection for revision.
        
        Args:
            selection_id: Reviewer selection ID
            mentor_feedback: Mentor feedback
            
        Returns:
            Optional[ReviewerSelection]: Updated reviewer selection object if found, None otherwise
        """
        db_selection = self.get_by_id(selection_id)
        if not db_selection:
            return None
        
        db_selection.status = "sent_back"
        db_selection.mentor_feedback = mentor_feedback
        
        self.db.commit()
        self.db.refresh(db_selection)
        return db_selection
    
    def delete(self, selection_id: int) -> bool:
        """
        Delete reviewer selection by ID.
        
        Args:
            selection_id: Reviewer selection ID
            
        Returns:
            bool: True if reviewer selection was deleted, False if not found
        """
        db_selection = self.get_by_id(selection_id)
        if not db_selection:
            return False
        
        self.db.delete(db_selection)
        self.db.commit()
        return True
    
    def get_selected_reviewers(self, selection_id: int) -> List[User]:
        """
        Get selected reviewers for a selection.
        
        Args:
            selection_id: Reviewer selection ID
            
        Returns:
            List[User]: List of selected reviewers
        """
        return self.db.query(User).join(ReviewerSelectionDetail).filter(
            ReviewerSelectionDetail.selection_id == selection_id
        ).all()
