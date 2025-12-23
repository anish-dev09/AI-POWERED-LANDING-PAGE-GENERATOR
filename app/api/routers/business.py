"""
Business API router - CRUD operations for businesses.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import business as business_crud
from app.schemas.business import BusinessCreate, BusinessUpdate, BusinessResponse


router = APIRouter(prefix="/businesses", tags=["businesses"])


@router.post("/", response_model=BusinessResponse, status_code=201)
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new business.
    
    Args:
        business: Business data
        db: Database session
        
    Returns:
        Created business
    """
    try:
        db_business = business_crud.create_business(db, business)
        return db_business
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating business: {str(e)}")


@router.get("/", response_model=List[BusinessResponse])
def list_businesses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name or industry"),
    db: Session = Depends(get_db)
):
    """
    List all businesses with pagination and search.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search term
        db: Database session
        
    Returns:
        List of businesses
    """
    try:
        businesses = business_crud.get_businesses(db, skip=skip, limit=limit, search=search)
        return businesses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching businesses: {str(e)}")


@router.get("/{business_id}", response_model=BusinessResponse)
def get_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific business by ID.
    
    Args:
        business_id: Business ID
        db: Database session
        
    Returns:
        Business data
    """
    db_business = business_crud.get_business(db, business_id)
    if not db_business:
        raise HTTPException(status_code=404, detail="Business not found")
    return db_business


@router.put("/{business_id}", response_model=BusinessResponse)
def update_business(
    business_id: int,
    business_update: BusinessUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a business.
    
    Args:
        business_id: Business ID
        business_update: Updated business data
        db: Database session
        
    Returns:
        Updated business
    """
    db_business = business_crud.get_business(db, business_id)
    if not db_business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    try:
        # Only include fields that were actually set
        update_data = business_update.model_dump(exclude_unset=True)
        # Convert to BusinessUpdate schema
        updated_business = business_crud.update_business(db, business_id, business_update)
        return updated_business
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating business: {str(e)}")


@router.delete("/{business_id}", status_code=204)
def delete_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a business.
    
    Args:
        business_id: Business ID
        db: Database session
        
    Returns:
        No content
    """
    db_business = business_crud.get_business(db, business_id)
    if not db_business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    try:
        business_crud.delete_business(db, business_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting business: {str(e)}")


@router.get("/stats/count")
def get_business_count(
    db: Session = Depends(get_db)
):
    """
    Get total count of businesses.
    
    Args:
        db: Database session
        
    Returns:
        Count of businesses
    """
    try:
        count = business_crud.get_business_count(db)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting businesses: {str(e)}")
