"""
Performance Cycle API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.performance_cycle_service import PerformanceCycleService
from app.schemas.performance_cycle import (
    PerformanceCycleCreate,
    PerformanceCycleUpdate,
    PerformanceCycleResponse
)
from app.api.dependencies import get_current_user, get_current_superuser
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/active", response_model=PerformanceCycleResponse)
def get_active_performance_cycle(
    db: Session = Depends(get_db)
) -> PerformanceCycleResponse:
    """
    Get active performance cycle.
    
    Args:
        db: Database session
        
    Returns:
        PerformanceCycleResponse: Active performance cycle data
        
    Raises:
        HTTPException: If no active cycle found
    """
    cycle_service = PerformanceCycleService(db)
    cycle = cycle_service.get_active_cycle()
    
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active performance cycle found"
        )
    
    return cycle


@router.get("/", response_model=List[PerformanceCycleResponse])
def get_performance_cycles(
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> List[PerformanceCycleResponse]:
    """
    Get all performance cycles with optional filtering (Admin/HR only).
    
    Args:
        status: Filter by status
        page: Page number
        limit: Items per page
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[PerformanceCycleResponse]: List of performance cycles
    """
    skip = (page - 1) * limit
    cycle_service = PerformanceCycleService(db)
    cycles = cycle_service.get_all_cycles(skip=skip, limit=limit, status=status)
    
    return cycles


@router.post("/", response_model=PerformanceCycleResponse)
def create_performance_cycle(
    cycle_create: PerformanceCycleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> PerformanceCycleResponse:
    """
    Create a new performance cycle (Admin/HR only).
    
    Args:
        cycle_create: Performance cycle creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PerformanceCycleResponse: Created performance cycle data
    """
    cycle_service = PerformanceCycleService(db)
    cycle = cycle_service.create_cycle(cycle_create)
    
    logger.info("Performance cycle created", cycle_id=cycle.id, created_by=current_user.id)
    
    return cycle


@router.get("/{cycle_id}", response_model=PerformanceCycleResponse)
def get_performance_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> PerformanceCycleResponse:
    """
    Get performance cycle by ID (Admin/HR only).
    
    Args:
        cycle_id: Performance cycle ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PerformanceCycleResponse: Performance cycle data
    """
    cycle_service = PerformanceCycleService(db)
    cycle = cycle_service.get_cycle_by_id(cycle_id)
    
    return cycle


@router.put("/{cycle_id}", response_model=PerformanceCycleResponse)
def update_performance_cycle(
    cycle_id: int,
    cycle_update: PerformanceCycleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> PerformanceCycleResponse:
    """
    Update performance cycle (Admin/HR only).
    
    Args:
        cycle_id: Performance cycle ID
        cycle_update: Performance cycle update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PerformanceCycleResponse: Updated performance cycle data
    """
    cycle_service = PerformanceCycleService(db)
    cycle = cycle_service.update_cycle(cycle_id, cycle_update)
    
    logger.info("Performance cycle updated", cycle_id=cycle_id, updated_by=current_user.id)
    
    return cycle


@router.delete("/{cycle_id}")
def delete_performance_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete performance cycle (Admin/HR only).
    
    Args:
        cycle_id: Performance cycle ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    cycle_service = PerformanceCycleService(db)
    success = cycle_service.delete_cycle(cycle_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance cycle not found"
        )
    
    logger.info("Performance cycle deleted", cycle_id=cycle_id, deleted_by=current_user.id)
    
    return {"message": "Performance cycle deleted successfully"}
