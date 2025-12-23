"""
Landing Page API router - Generation and management endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import landing_page as page_crud
from app.schemas.landing_page import (
    PageCustomization, 
    LandingPageResponse,
    PageUpdate
)
from app.services.landing_page_service import get_landing_page_service


router = APIRouter(prefix="/landing-pages", tags=["landing-pages"])


@router.post("/generate/{business_id}", response_model=LandingPageResponse, status_code=201)
async def generate_landing_page(
    business_id: int,
    customization: Optional[PageCustomization] = None,
    db: Session = Depends(get_db)
):
    """
    Generate a new landing page for a business using AI.
    
    Args:
        business_id: Business ID
        customization: Optional customization settings
        db: Database session
        
    Returns:
        Generated landing page with HTML/CSS file paths
    """
    try:
        service = get_landing_page_service()
        result = await service.generate_landing_page(
            db=db,
            business_id=business_id,
            customization=customization
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating landing page: {str(e)}")


@router.get("/", response_model=List[LandingPageResponse])
def list_landing_pages(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    business_id: Optional[int] = Query(None, description="Filter by business ID"),
    published_only: bool = Query(False, description="Only return published pages"),
    db: Session = Depends(get_db)
):
    """
    List all landing pages with pagination and filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        business_id: Optional business ID filter
        published_only: Only return published pages
        db: Database session
        
    Returns:
        List of landing pages
    """
    try:
        pages = page_crud.get_landing_pages(
            db,
            business_id=business_id,
            published_only=published_only,
            skip=skip,
            limit=limit
        )
        
        # Convert to response format
        return [
            {
                "id": page.id,
                "business_id": page.business_id,
                "version": page.version,
                "headline": page.headline,
                "subheadline": page.subheadline,
                "cta_text": page.cta_text,
                "features": page.get_features(),
                "testimonials": page.get_testimonials(),
                "meta_title": page.meta_title,
                "meta_description": page.meta_description,
                "keywords": page.get_keywords(),
                "og_title": page.og_title,
                "og_description": page.og_description,
                "theme": page.theme,
                "primary_color": page.primary_color,
                "secondary_color": page.secondary_color,
                "html_path": page.html_path,
                "css_path": page.css_path,
                "is_published": page.is_published,
                "view_count": page.view_count,
                "created_at": page.created_at,
                "updated_at": page.updated_at
            }
            for page in pages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching landing pages: {str(e)}")


@router.get("/{page_id}", response_model=LandingPageResponse)
def get_landing_page(
    page_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific landing page by ID.
    
    Args:
        page_id: Landing page ID
        db: Database session
        
    Returns:
        Landing page data
    """
    page = page_crud.get_landing_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    return {
        "id": page.id,
        "business_id": page.business_id,
        "version": page.version,
        "headline": page.headline,
        "subheadline": page.subheadline,
        "cta_text": page.cta_text,
        "features": page.get_features(),
        "testimonials": page.get_testimonials(),
        "meta_title": page.meta_title,
        "meta_description": page.meta_description,
        "keywords": page.get_keywords(),
        "og_title": page.og_title,
        "og_description": page.og_description,
        "theme": page.theme,
        "primary_color": page.primary_color,
        "secondary_color": page.secondary_color,
        "html_path": page.html_path,
        "css_path": page.css_path,
        "is_published": page.is_published,
        "view_count": page.view_count,
        "created_at": page.created_at,
        "updated_at": page.updated_at
    }


@router.put("/{page_id}", response_model=LandingPageResponse)
def update_landing_page(
    page_id: int,
    page_update: PageUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a landing page.
    
    Args:
        page_id: Landing page ID
        page_update: Updated page data
        db: Database session
        
    Returns:
        Updated landing page
    """
    page = page_crud.get_landing_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    try:
        # Only include fields that were actually set
        update_data = page_update.model_dump(exclude_unset=True)
        updated_page = page_crud.update_landing_page(db, page_id, update_data)  # type: ignore
        
        return {
            "id": updated_page.id,
            "business_id": updated_page.business_id,
            "version": updated_page.version,
            "headline": updated_page.headline,
            "subheadline": updated_page.subheadline,
            "cta_text": updated_page.cta_text,
            "features": updated_page.get_features(),
            "testimonials": updated_page.get_testimonials(),
            "meta_title": updated_page.meta_title,
            "meta_description": updated_page.meta_description,
            "keywords": updated_page.get_keywords(),
            "og_title": updated_page.og_title,
            "og_description": updated_page.og_description,
            "theme": updated_page.theme,
            "primary_color": updated_page.primary_color,
            "secondary_color": updated_page.secondary_color,
            "html_path": updated_page.html_path,
            "css_path": updated_page.css_path,
            "is_published": updated_page.is_published,
            "view_count": updated_page.view_count,
            "created_at": updated_page.created_at,
            "updated_at": updated_page.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating landing page: {str(e)}")


@router.delete("/{page_id}", status_code=204)
def delete_landing_page(
    page_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a landing page.
    
    Args:
        page_id: Landing page ID
        db: Database session
        
    Returns:
        No content
    """
    page = page_crud.get_landing_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    try:
        page_crud.delete_landing_page(db, page_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting landing page: {str(e)}")


@router.post("/{page_id}/publish", response_model=LandingPageResponse)
def publish_landing_page(
    page_id: int,
    db: Session = Depends(get_db)
):
    """
    Publish a landing page (make it publicly visible).
    
    Args:
        page_id: Landing page ID
        db: Database session
        
    Returns:
        Updated landing page
    """
    page = page_crud.get_landing_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    try:
        updated_page = page_crud.publish_landing_page(db, page_id)  # type: ignore
        
        return {
            "id": updated_page.id,
            "business_id": updated_page.business_id,
            "version": updated_page.version,
            "headline": updated_page.headline,
            "subheadline": updated_page.subheadline,
            "cta_text": updated_page.cta_text,
            "features": updated_page.get_features(),
            "testimonials": updated_page.get_testimonials(),
            "meta_title": updated_page.meta_title,
            "meta_description": updated_page.meta_description,
            "keywords": updated_page.get_keywords(),
            "og_title": updated_page.og_title,
            "og_description": updated_page.og_description,
            "theme": updated_page.theme,
            "primary_color": updated_page.primary_color,
            "secondary_color": updated_page.secondary_color,
            "html_path": updated_page.html_path,
            "css_path": updated_page.css_path,
            "is_published": updated_page.is_published,
            "view_count": updated_page.view_count,
            "created_at": updated_page.created_at,
            "updated_at": updated_page.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing landing page: {str(e)}")


@router.post("/{page_id}/unpublish", response_model=LandingPageResponse)
def unpublish_landing_page(
    page_id: int,
    db: Session = Depends(get_db)
):
    """
    Unpublish a landing page (hide from public).
    
    Args:
        page_id: Landing page ID
        db: Database session
        
    Returns:
        Updated landing page
    """
    page = page_crud.get_landing_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    try:
        updated_page = page_crud.unpublish_landing_page(db, page_id)  # type: ignore
        
        return {
            "id": updated_page.id,
            "business_id": updated_page.business_id,
            "version": updated_page.version,
            "headline": updated_page.headline,
            "subheadline": updated_page.subheadline,
            "cta_text": updated_page.cta_text,
            "features": updated_page.get_features(),
            "testimonials": updated_page.get_testimonials(),
            "meta_title": updated_page.meta_title,
            "meta_description": updated_page.meta_description,
            "keywords": updated_page.get_keywords(),
            "og_title": updated_page.og_title,
            "og_description": updated_page.og_description,
            "theme": updated_page.theme,
            "primary_color": updated_page.primary_color,
            "secondary_color": updated_page.secondary_color,
            "html_path": updated_page.html_path,
            "css_path": updated_page.css_path,
            "is_published": updated_page.is_published,
            "view_count": updated_page.view_count,
            "created_at": updated_page.created_at,
            "updated_at": updated_page.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error unpublishing landing page: {str(e)}")


@router.post("/{page_id}/view", status_code=204)
def track_page_view(
    page_id: int,
    db: Session = Depends(get_db)
):
    """
    Track a view for a landing page (increment view counter).
    
    Args:
        page_id: Landing page ID
        db: Database session
        
    Returns:
        No content
    """
    page = page_crud.get_landing_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    try:
        page_crud.increment_view_count(db, page_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking view: {str(e)}")


@router.get("/stats/count")
def get_landing_page_count(
    business_id: Optional[int] = Query(None, description="Filter by business ID"),
    db: Session = Depends(get_db)
):
    """
    Get total count of landing pages.
    
    Args:
        business_id: Optional business ID filter
        db: Database session
        
    Returns:
        Count of landing pages
    """
    try:
        count = page_crud.get_landing_page_count(db, business_id=business_id)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting landing pages: {str(e)}")
