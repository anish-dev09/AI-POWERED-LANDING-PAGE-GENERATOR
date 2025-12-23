"""
Landing Page Service - Orchestrates AI generation and database operations.
"""
import json
import os
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.crud.business import get_business
from app.crud.landing_page import create_landing_page
from app.services.content_generator import get_content_service
from app.schemas.landing_page import PageCustomization


class LandingPageService:
    """Service for orchestrating landing page generation."""
    
    def __init__(self):
        """Initialize the landing page service."""
        self.content_service = get_content_service()
    
    async def generate_landing_page(
        self,
        db: Session,
        business_id: int,
        customization: Optional[PageCustomization] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete landing page for a business.
        
        Args:
            db: Database session
            business_id: ID of the business
            customization: Optional customization settings
            
        Returns:
            Dictionary with generated landing page data
            
        Raises:
            ValueError: If business not found
            Exception: If generation fails
        """
        # Get business data
        business = get_business(db, business_id)
        if not business:
            raise ValueError(f"Business with ID {business_id} not found")
        
        # Prepare business data
        business_data = {
            "name": business.name,
            "industry": business.industry,
            "target_audience": business.target_audience,
            "tone": business.tone,
            "goal": business.goal,
            "unique_value_proposition": business.unique_value_proposition,
            "additional_info": business.additional_info
        }
        
        # Use default customization if not provided
        if customization is None:
            customization = PageCustomization()
        
        # Generate content using AI
        print(f"🤖 Generating landing page content for {business.name}...")
        
        if customization.include_features and customization.include_testimonials:
            # Generate everything in one call (more efficient)
            content = await self.content_service.generate_complete_landing_page(
                business_data,
                num_features=customization.num_features if customization.include_features else 0,
                num_testimonials=customization.num_testimonials if customization.include_testimonials else 0
            )
        else:
            # Generate components separately if some are disabled
            content = await self._generate_partial_content(
                business_data,
                customization
            )
        
        # Prepare landing page data
        page_data = {
            "headline": content.get("headline", ""),
            "subheadline": content.get("subheadline"),
            "cta_text": content.get("cta_text", "Get Started"),
            "features": json.dumps(content.get("features", [])) if customization.include_features else None,
            "testimonials": json.dumps(content.get("testimonials", [])) if customization.include_testimonials else None,
            "meta_title": content.get("meta_title"),
            "meta_description": content.get("meta_description"),
            "keywords": json.dumps(content.get("keywords", [])),
            "og_title": content.get("og_title"),
            "og_description": content.get("og_description"),
            "theme": customization.theme,
            "primary_color": customization.primary_color,
            "secondary_color": customization.secondary_color,
            "html_path": None,  # Will be set when HTML is generated
            "css_path": None,  # Will be set when CSS is generated
            "is_published": False,
            "view_count": 0
        }
        
        # Save to database
        db_page = create_landing_page(db, business_id, page_data)
        
        print(f"✓ Landing page generated successfully (ID: {db_page.id})")
        
        # Return the page data with parsed JSON for easy use
        return {
            "id": db_page.id,
            "business_id": db_page.business_id,
            "headline": db_page.headline,
            "subheadline": db_page.subheadline,
            "cta_text": db_page.cta_text,
            "features": db_page.get_features(),
            "testimonials": db_page.get_testimonials(),
            "meta_title": db_page.meta_title,
            "meta_description": db_page.meta_description,
            "keywords": db_page.get_keywords(),
            "theme": db_page.theme,
            "primary_color": db_page.primary_color,
            "secondary_color": db_page.secondary_color,
            "created_at": db_page.created_at
        }
    
    async def _generate_partial_content(
        self,
        business_data: Dict[str, Any],
        customization: PageCustomization
    ) -> Dict[str, Any]:
        """
        Generate landing page content with some components disabled.
        
        Args:
            business_data: Business information
            customization: Customization settings
            
        Returns:
            Dictionary with generated content
        """
        content = {}
        
        # Generate headline and subheadline
        headline = await self.content_service.generate_headline(business_data)
        content["headline"] = headline
        content["subheadline"] = f"Discover how {business_data['name']} can help you achieve your goals."
        content["cta_text"] = "Get Started"
        
        # Generate features if enabled
        if customization.include_features:
            features = await self.content_service.generate_features(
                business_data,
                customization.num_features
            )
            content["features"] = features
        else:
            content["features"] = []
        
        # Generate testimonials if enabled
        if customization.include_testimonials:
            testimonials = await self.content_service.generate_testimonials(
                business_data,
                customization.num_testimonials
            )
            content["testimonials"] = testimonials
        else:
            content["testimonials"] = []
        
        # Generate SEO metadata
        seo = await self.content_service.generate_seo_metadata(business_data, headline)
        content.update(seo)
        
        return content
    
    def get_output_directory(self) -> str:
        """Get the directory for generated landing pages."""
        output_dir = os.path.join(os.getcwd(), "generated_pages")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir


# Singleton instance
_landing_page_service = None


def get_landing_page_service() -> LandingPageService:
    """Get or create the landing page service instance."""
    global _landing_page_service
    if _landing_page_service is None:
        _landing_page_service = LandingPageService()
    return _landing_page_service
