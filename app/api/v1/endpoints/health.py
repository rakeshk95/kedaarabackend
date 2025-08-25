"""
Health check endpoints.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Performance Review API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/health/detailed")
def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with database connectivity test.
    
    Args:
        db: Database session
        
    Returns:
        dict: Detailed health status information
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Performance Review API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": db_status,
            "url": settings.DATABASE_URL.split("@")[1].split("/")[0] if "@" in settings.DATABASE_URL else "configured"
        },
        "features": {
            "authentication": "enabled",
            "logging": "enabled",
            "cors": "enabled"
        }
    }
