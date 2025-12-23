"""
Health check and system status endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db
from app.crud import business as business_crud
from app.crud import landing_page as page_crud


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Landing Page Generator"
    }


@router.get("/detailed")
def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with database connectivity and system stats.
    
    Args:
        db: Database session
        
    Returns:
        Detailed health status
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Landing Page Generator",
        "checks": {}
    }
    
    # Check database connectivity
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
    
    # Get system statistics
    try:
        business_count = business_crud.get_business_count(db)
        page_count = page_crud.get_landing_page_count(db)
        
        health_status["checks"]["statistics"] = {
            "status": "healthy",
            "data": {
                "total_businesses": business_count,
                "total_landing_pages": page_count
            }
        }
    except Exception as e:
        health_status["checks"]["statistics"] = {
            "status": "partial",
            "message": f"Could not fetch statistics: {str(e)}"
        }
    
    return health_status


@router.get("/version")
def version_info():
    """
    Get API version information.
    
    Returns:
        Version details
    """
    return {
        "version": "1.0.0",
        "api_version": "v1",
        "service": "AI Landing Page Generator",
        "description": "AI-powered landing page generation service"
    }
