"""
Performance Cycle service for business logic operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.performance_cycle_repository import PerformanceCycleRepository
from app.schemas.performance_cycle import PerformanceCycleCreate, PerformanceCycleUpdate, PerformanceCycleResponse
from app.utils.exceptions import PerformanceCycleNotFoundException, ValidationException


class PerformanceCycleService:
    """Service for performance cycle business logic operations."""
    
    def __init__(self, db: Session):
        self.repository = PerformanceCycleRepository(db)
    
    def get_active_cycle(self) -> Optional[PerformanceCycleResponse]:
        """
        Get active performance cycle.
        
        Returns:
            Optional[PerformanceCycleResponse]: Active performance cycle if found, None otherwise
        """
        cycle = self.repository.get_active_cycle()
        if not cycle:
            return None
        return PerformanceCycleResponse.from_orm(cycle)
    
    def get_cycle_by_id(self, cycle_id: int) -> PerformanceCycleResponse:
        """
        Get performance cycle by ID.
        
        Args:
            cycle_id: Performance cycle ID
            
        Returns:
            PerformanceCycleResponse: Performance cycle data
            
        Raises:
            PerformanceCycleNotFoundException: If performance cycle not found
        """
        cycle = self.repository.get_by_id(cycle_id)
        if not cycle:
            raise PerformanceCycleNotFoundException(f"Performance cycle with ID {cycle_id} not found")
        return PerformanceCycleResponse.from_orm(cycle)
    
    def get_all_cycles(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[PerformanceCycleResponse]:
        """
        Get all performance cycles with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[PerformanceCycleResponse]: List of performance cycles
        """
        cycles = self.repository.get_all(skip=skip, limit=limit, status=status)
        return [PerformanceCycleResponse.from_orm(cycle) for cycle in cycles]
    
    def create_cycle(self, cycle_create: PerformanceCycleCreate) -> PerformanceCycleResponse:
        """
        Create a new performance cycle.
        
        Args:
            cycle_create: Performance cycle creation data
            
        Returns:
            PerformanceCycleResponse: Created performance cycle data
            
        Raises:
            ValidationException: If validation fails
        """
        # Validate that start_date is before end_date
        if cycle_create.start_date >= cycle_create.end_date:
            raise ValidationException("Start date must be before end date")
        
        # If creating an active cycle, deactivate other active cycles
        if cycle_create.status == "active":
            active_cycle = self.repository.get_active_cycle()
            if active_cycle:
                # Deactivate the current active cycle
                self.repository.update(active_cycle.id, PerformanceCycleUpdate(status="inactive"))
        
        cycle = self.repository.create(cycle_create)
        return PerformanceCycleResponse.from_orm(cycle)
    
    def update_cycle(self, cycle_id: int, cycle_update: PerformanceCycleUpdate) -> PerformanceCycleResponse:
        """
        Update performance cycle information.
        
        Args:
            cycle_id: Performance cycle ID
            cycle_update: Performance cycle update data
            
        Returns:
            PerformanceCycleResponse: Updated performance cycle data
            
        Raises:
            PerformanceCycleNotFoundException: If performance cycle not found
            ValidationException: If validation fails
        """
        # Validate that start_date is before end_date if both are provided
        if cycle_update.start_date and cycle_update.end_date:
            if cycle_update.start_date >= cycle_update.end_date:
                raise ValidationException("Start date must be before end date")
        
        cycle = self.repository.update(cycle_id, cycle_update)
        if not cycle:
            raise PerformanceCycleNotFoundException(f"Performance cycle with ID {cycle_id} not found")
        
        # If updating to active status, deactivate other active cycles
        if cycle_update.status == "active":
            active_cycle = self.repository.get_active_cycle()
            if active_cycle and active_cycle.id != cycle_id:
                # Deactivate the current active cycle
                self.repository.update(active_cycle.id, PerformanceCycleUpdate(status="inactive"))
        
        return PerformanceCycleResponse.from_orm(cycle)
    
    def delete_cycle(self, cycle_id: int) -> bool:
        """
        Delete performance cycle by ID.
        
        Args:
            cycle_id: Performance cycle ID
            
        Returns:
            bool: True if performance cycle was deleted, False if not found
        """
        return self.repository.delete(cycle_id)
