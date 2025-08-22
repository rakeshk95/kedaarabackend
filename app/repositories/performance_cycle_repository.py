"""
Performance Cycle repository for database operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.performance_cycle import PerformanceCycle
from app.schemas.performance_cycle import PerformanceCycleCreate, PerformanceCycleUpdate


class PerformanceCycleRepository:
    """Repository for performance cycle database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, cycle_id: int) -> Optional[PerformanceCycle]:
        """
        Get performance cycle by ID.
        
        Args:
            cycle_id: Performance cycle ID
            
        Returns:
            Optional[PerformanceCycle]: Performance cycle object if found, None otherwise
        """
        return self.db.query(PerformanceCycle).filter(PerformanceCycle.id == cycle_id).first()
    
    def get_active_cycle(self) -> Optional[PerformanceCycle]:
        """
        Get active performance cycle.
        
        Returns:
            Optional[PerformanceCycle]: Active performance cycle if found, None otherwise
        """
        return self.db.query(PerformanceCycle).filter(PerformanceCycle.status == "active").first()
    
    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[PerformanceCycle]:
        """
        Get all performance cycles with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            
        Returns:
            List[PerformanceCycle]: List of performance cycles
        """
        query = self.db.query(PerformanceCycle)
        if status:
            query = query.filter(PerformanceCycle.status == status)
        return query.offset(skip).limit(limit).all()
    
    def create(self, cycle_create: PerformanceCycleCreate) -> PerformanceCycle:
        """
        Create a new performance cycle.
        
        Args:
            cycle_create: Performance cycle creation data
            
        Returns:
            PerformanceCycle: Created performance cycle object
        """
        db_cycle = PerformanceCycle(
            name=cycle_create.name,
            start_date=cycle_create.start_date,
            end_date=cycle_create.end_date,
            status=cycle_create.status,
            description=cycle_create.description
        )
        self.db.add(db_cycle)
        self.db.commit()
        self.db.refresh(db_cycle)
        return db_cycle
    
    def update(self, cycle_id: int, cycle_update: PerformanceCycleUpdate) -> Optional[PerformanceCycle]:
        """
        Update performance cycle information.
        
        Args:
            cycle_id: Performance cycle ID
            cycle_update: Performance cycle update data
            
        Returns:
            Optional[PerformanceCycle]: Updated performance cycle object if found, None otherwise
        """
        db_cycle = self.get_by_id(cycle_id)
        if not db_cycle:
            return None
        
        update_data = cycle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cycle, field, value)
        
        self.db.commit()
        self.db.refresh(db_cycle)
        return db_cycle
    
    def delete(self, cycle_id: int) -> bool:
        """
        Delete performance cycle by ID.
        
        Args:
            cycle_id: Performance cycle ID
            
        Returns:
            bool: True if performance cycle was deleted, False if not found
        """
        db_cycle = self.get_by_id(cycle_id)
        if not db_cycle:
            return False
        
        self.db.delete(db_cycle)
        self.db.commit()
        return True
