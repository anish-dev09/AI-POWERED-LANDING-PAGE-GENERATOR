"""
CRUD operations for LandingPage model.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.landing_page import LandingPage
from app.schemas.landing_page import PageUpdate


def create_landing_page(
    db: Session,
    business_id: int,
    page_data: dict
) -> LandingPage:
    """
    Create a new landing page.
    
    Args:
        db: Database session
        business_id: Business ID
        page_data: Landing page data
        
    Returns:
        Created LandingPage instance
    """
    db_page = LandingPage(business_id=business_id, **page_data)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page


def get_landing_page(db: Session, page_id: int) -> Optional[LandingPage]:
    """
    Get a landing page by ID.
    
    Args:
        db: Database session
        page_id: Landing page ID
        
    Returns:
        LandingPage instance or None
    """
    return db.query(LandingPage).filter(LandingPage.id == page_id).first()  # type: ignore


def get_landing_pages(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    business_id: Optional[int] = None,
    published_only: bool = False
) -> List[LandingPage]:
    """
    Get list of landing pages with pagination and optional filters.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        business_id: Optional filter by business ID
        published_only: If True, only return published pages
        
    Returns:
        List of LandingPage instances
    """
    query = db.query(LandingPage)
    
    if business_id:
        query = query.filter(LandingPage.business_id == business_id)  # type: ignore
    
    if published_only:
        query = query.filter(LandingPage.is_published == True)  # type: ignore
    
    return query.order_by(desc(LandingPage.created_at)).offset(skip).limit(limit).all()  # type: ignore


def update_landing_page(
    db: Session,
    page_id: int,
    page_data: PageUpdate
) -> Optional[LandingPage]:
    """
    Update a landing page.
    
    Args:
        db: Database session
        page_id: Landing page ID
        page_data: Page update data
        
    Returns:
        Updated LandingPage instance or None
    """
    db_page = get_landing_page(db, page_id)
    if not db_page:
        return None
    
    # Update only provided fields
    update_data = page_data.model_dump(exclude_unset=True)
    
    # Handle nested objects (features, testimonials)
    if "features" in update_data and update_data["features"]:
        import json
        update_data["features"] = json.dumps([f.model_dump() for f in update_data["features"]])
    
    if "testimonials" in update_data and update_data["testimonials"]:
        import json
        update_data["testimonials"] = json.dumps([t.model_dump() for t in update_data["testimonials"]])
    
    if "keywords" in update_data and update_data["keywords"]:
        import json
        update_data["keywords"] = json.dumps(update_data["keywords"])
    
    for field, value in update_data.items():
        setattr(db_page, field, value)
    
    db.commit()
    db.refresh(db_page)
    return db_page


def delete_landing_page(db: Session, page_id: int) -> bool:
    """
    Delete a landing page.
    
    Args:
        db: Database session
        page_id: Landing page ID
        
    Returns:
        True if deleted, False if not found
    """
    db_page = get_landing_page(db, page_id)
    if not db_page:
        return False
    
    db.delete(db_page)
    db.commit()
    return True


def publish_landing_page(db: Session, page_id: int) -> Optional[LandingPage]:
    """
    Publish a landing page.
    
    Args:
        db: Database session
        page_id: Landing page ID
        
    Returns:
        Updated LandingPage instance or None
    """
    db_page = get_landing_page(db, page_id)
    if not db_page:
        return None
    
    db_page.is_published = True
    db.commit()
    db.refresh(db_page)
    return db_page


def unpublish_landing_page(db: Session, page_id: int) -> Optional[LandingPage]:
    """
    Unpublish a landing page.
    
    Args:
        db: Database session
        page_id: Landing page ID
        
    Returns:
        Updated LandingPage instance or None
    """
    db_page = get_landing_page(db, page_id)
    if not db_page:
        return None
    
    db_page.is_published = False
    db.commit()
    db.refresh(db_page)
    return db_page


def increment_view_count(db: Session, page_id: int) -> Optional[LandingPage]:
    """
    Increment the view count of a landing page.
    
    Args:
        db: Database session
        page_id: Landing page ID
        
    Returns:
        Updated LandingPage instance or None
    """
    db_page = get_landing_page(db, page_id)
    if not db_page:
        return None
    
    db_page.view_count += 1
    db.commit()
    db.refresh(db_page)
    return db_page


def get_landing_page_count(
    db: Session,
    business_id: Optional[int] = None,
    published_only: bool = False
) -> int:
    """
    Get total count of landing pages.
    
    Args:
        db: Database session
        business_id: Optional filter by business ID
        published_only: If True, only count published pages
        
    Returns:
        Total number of landing pages
    """
    query = db.query(LandingPage)
    
    if business_id:
        query = query.filter(LandingPage.business_id == business_id)  # type: ignore
    
    if published_only:
        query = query.filter(LandingPage.is_published == True)  # type: ignore
    
    return query.count()
