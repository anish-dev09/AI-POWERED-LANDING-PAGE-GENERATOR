"""
Landing Page model - stores generated landing page data
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from app.database import Base
import json

if TYPE_CHECKING:
    from app.models.business import Business


class LandingPage(Base):
    """
    Landing Page model representing a generated landing page.
    
    Attributes:
        id: Primary key
        business_id: Foreign key to Business
        version: Version number for this business
        
        Content Fields:
        headline: Main headline text
        subheadline: Supporting subheadline
        cta_text: Call-to-action button text
        features: JSON string of features list
        testimonials: JSON string of testimonials
        about_section: About section content
        
        SEO Fields:
        meta_title: SEO title tag
        meta_description: SEO meta description
        keywords: SEO keywords (JSON array)
        og_title: Open Graph title
        og_description: Open Graph description
        
        Design Fields:
        theme: Theme name (modern, minimal, corporate)
        primary_color: Primary color hex code
        secondary_color: Secondary color hex code
        
        File Paths:
        html_path: Path to generated HTML file
        css_path: Path to generated CSS file
        
        Metadata:
        is_published: Whether page is published
        view_count: Number of times viewed
        created_at: Creation timestamp
        updated_at: Last update timestamp
        
    Relationships:
        business: The business this page belongs to
    """
    
    __tablename__ = "landing_pages"
    
    # Primary Key
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)  # type: ignore
    
    # Foreign Keys
    business_id: int = Column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)  # type: ignore
    
    # Version Control
    version: int = Column(Integer, default=1, nullable=False)  # type: ignore
    
    # Content Fields
    headline: str = Column(String(200), nullable=False)  # type: ignore
    subheadline: Optional[str] = Column(Text, nullable=True)  # type: ignore
    cta_text: str = Column(String(100), default="Get Started")  # type: ignore
    features: Optional[str] = Column(Text, nullable=True)  # type: ignore  # JSON string
    testimonials: Optional[str] = Column(Text, nullable=True)  # type: ignore  # JSON string
    about_section: Optional[str] = Column(Text, nullable=True)  # type: ignore
    
    # SEO Fields
    meta_title: Optional[str] = Column(String(60), nullable=True)  # type: ignore
    meta_description: Optional[str] = Column(String(160), nullable=True)  # type: ignore
    keywords: Optional[str] = Column(Text, nullable=True)  # type: ignore  # JSON array
    og_title: Optional[str] = Column(String(100), nullable=True)  # type: ignore
    og_description: Optional[str] = Column(String(200), nullable=True)  # type: ignore
    
    # Design Fields
    theme: str = Column(String(50), default="modern")  # type: ignore
    primary_color: str = Column(String(7), default="#3B82F6")  # type: ignore  # Hex color
    secondary_color: str = Column(String(7), default="#1E40AF")  # type: ignore
    
    # File Paths
    html_path: Optional[str] = Column(String(255), nullable=True)  # type: ignore
    css_path: Optional[str] = Column(String(255), nullable=True)  # type: ignore
    
    # Metadata
    is_published: bool = Column(Boolean, default=False)  # type: ignore
    view_count: int = Column(Integer, default=0)  # type: ignore
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)  # type: ignore
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # type: ignore
    
    # Relationships (no type hint to avoid SQLAlchemy conflicts)
    business = relationship("Business", back_populates="landing_pages")
    
    def __repr__(self):
        return f"<LandingPage(id={self.id}, business_id={self.business_id}, headline='{self.headline[:30]}...')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "business_id": self.business_id,
            "version": self.version,
            "headline": self.headline,
            "subheadline": self.subheadline,
            "cta_text": self.cta_text,
            "features": json.loads(self.features) if self.features else [],
            "testimonials": json.loads(self.testimonials) if self.testimonials else [],
            "about_section": self.about_section,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "keywords": json.loads(self.keywords) if self.keywords else [],
            "og_title": self.og_title,
            "og_description": self.og_description,
            "theme": self.theme,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "html_path": self.html_path,
            "css_path": self.css_path,
            "is_published": self.is_published,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def get_features(self):
        """Parse and return features as list"""
        try:
            return json.loads(self.features) if self.features else []
        except json.JSONDecodeError:
            return []
    
    def get_testimonials(self):
        """Parse and return testimonials as list"""
        try:
            return json.loads(self.testimonials) if self.testimonials else []
        except json.JSONDecodeError:
            return []
    
    def get_keywords(self):
        """Parse and return keywords as list"""
        try:
            return json.loads(self.keywords) if self.keywords else []
        except json.JSONDecodeError:
            return []
