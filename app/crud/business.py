"""
CRUD operations for Business model.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.business import Business
from app.schemas.business import BusinessInput, BusinessUpdate


def create_business(db: Session, business_data: BusinessInput) -> Business:
    """
    Create a new business.
    
    Args:
        db: Database session
        business_data: Business input data
        
    Returns:
        Created Business instance
    """
    db_business = Business(**business_data.model_dump())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def get_business(db: Session, business_id: int) -> Optional[Business]:
    """
    Get a business by ID.
    
    Args:
        db: Database session
        business_id: Business ID
        
    Returns:
        Business instance or None
    """
    return db.query(Business).filter(Business.id == business_id).first()  # type: ignore


def get_businesses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Business]:
    """
    Get list of businesses with pagination and optional search.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search term for name or industry
        
    Returns:
        List of Business instances
    """
    query = db.query(Business)
    
    if search:
        search_filter = or_(
            Business.name.ilike(f"%{search}%"),  # type: ignore
            Business.industry.ilike(f"%{search}%")  # type: ignore
        )
        query = query.filter(search_filter)  # type: ignore
    
    return query.offset(skip).limit(limit).all()


def update_business(
    db: Session,
    business_id: int,
    business_data: BusinessUpdate
) -> Optional[Business]:
    """
    Update a business.
    
    Args:
        db: Database session
        business_id: Business ID
        business_data: Business update data
        
    Returns:
        Updated Business instance or None
    """
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    
    # Update only provided fields
    update_data = business_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_business, field, value)
    
    db.commit()
    db.refresh(db_business)
    return db_business


def delete_business(db: Session, business_id: int) -> bool:
    """
    Delete a business.
    
    Args:
        db: Database session
        business_id: Business ID
        
    Returns:
        True if deleted, False if not found
    """
    db_business = get_business(db, business_id)
    if not db_business:
        return False
    
    db.delete(db_business)
    db.commit()
    return True


def get_business_count(db: Session) -> int:
    """
    Get total count of businesses.
    
    Args:
        db: Database session
        
    Returns:
        Total number of businesses
    """
    return db.query(Business).count()


def business_exists(db: Session, name: str, exclude_id: Optional[int] = None) -> bool:
    """
    Check if a business with the given name already exists.
    
    Args:
        db: Database session
        name: Business name to check
        exclude_id: Optional business ID to exclude from check (for updates)
        
    Returns:
        True if exists, False otherwise
    """
    query = db.query(Business).filter(Business.name == name)  # type: ignore
    if exclude_id:
        query = query.filter(Business.id != exclude_id)  # type: ignore
    return query.first() is not None
