"""
Landing Page related Pydantic schemas for request/response validation.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class FeatureItem(BaseModel):
    """Schema for a single feature."""
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    icon: Optional[str] = Field(None, max_length=50, description="Icon name or emoji")


class TestimonialItem(BaseModel):
    """Schema for a single testimonial."""
    name: str = Field(..., min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    content: str = Field(..., min_length=10, max_length=500)
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating out of 5")


class PageCustomization(BaseModel):
    """Schema for customizing landing page generation."""
    theme: str = Field(default="modern", max_length=50, description="Visual theme (modern, minimalist, bold, elegant)")
    primary_color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$", description="Primary color in hex format")
    secondary_color: str = Field(default="#10B981", pattern=r"^#[0-9A-Fa-f]{6}$", description="Secondary color in hex format")
    include_features: bool = Field(default=True, description="Include features section")
    include_testimonials: bool = Field(default=True, description="Include testimonials section")
    include_cta: bool = Field(default=True, description="Include call-to-action section")
    num_features: int = Field(default=3, ge=1, le=6, description="Number of features to generate")
    num_testimonials: int = Field(default=2, ge=0, le=5, description="Number of testimonials to generate")

    @field_validator('theme')
    @classmethod
    def validate_theme(cls, v: str) -> str:
        """Validate theme is one of the allowed values."""
        allowed_themes = ['modern', 'minimalist', 'bold', 'elegant', 'creative', 'corporate']
        if v.lower() not in allowed_themes:
            raise ValueError(f'Theme must be one of: {", ".join(allowed_themes)}')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "theme": "modern",
                "primary_color": "#3B82F6",
                "secondary_color": "#10B981",
                "include_features": True,
                "include_testimonials": True,
                "include_cta": True,
                "num_features": 3,
                "num_testimonials": 2
            }
        }


class PageGenerationRequest(BaseModel):
    """Complete request schema for generating a landing page."""
    business_id: int = Field(..., description="ID of the business to generate page for")
    customization: Optional[PageCustomization] = Field(default_factory=PageCustomization)


class PageOutput(BaseModel):
    """Schema for landing page response."""
    id: int
    business_id: int
    headline: str
    subheadline: Optional[str] = None
    cta_text: str
    cta_url: Optional[str] = None
    features: Optional[List[Dict[str, Any]]] = None
    testimonials: Optional[List[Dict[str, Any]]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    theme: str
    primary_color: str
    secondary_color: str
    html_path: Optional[str] = None
    css_path: Optional[str] = None
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Aliases for API compatibility
LandingPageResponse = PageOutput


class PageListOutput(BaseModel):
    """Schema for listing multiple landing pages."""
    total: int
    pages: List[PageOutput]


class PageUpdate(BaseModel):
    """Schema for updating landing page content."""
    headline: Optional[str] = Field(None, min_length=5, max_length=200)
    subheadline: Optional[str] = Field(None, max_length=300)
    cta_text: Optional[str] = Field(None, min_length=2, max_length=50)
    cta_url: Optional[str] = Field(None, max_length=500)
    features: Optional[List[FeatureItem]] = None
    testimonials: Optional[List[TestimonialItem]] = None
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    keywords: Optional[List[str]] = None
    og_title: Optional[str] = Field(None, max_length=60)
    og_description: Optional[str] = Field(None, max_length=200)
    theme: Optional[str] = None
    primary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_published: Optional[bool] = None

    @field_validator('theme')
    @classmethod
    def validate_theme(cls, v: Optional[str]) -> Optional[str]:
        """Validate theme if provided."""
        if v is None:
            return v
        allowed_themes = ['modern', 'minimalist', 'bold', 'elegant', 'creative', 'corporate']
        if v.lower() not in allowed_themes:
            raise ValueError(f'Theme must be one of: {", ".join(allowed_themes)}')
        return v.lower()


class PageStats(BaseModel):
    """Schema for landing page statistics."""
    page_id: int
    view_count: int
    is_published: bool
    created_at: datetime
    last_updated: datetime
