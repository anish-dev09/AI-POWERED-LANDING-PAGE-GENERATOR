"""
Landing Page model - stores generated landing page data
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import json


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
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    business_id = Column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Version Control
    version = Column(Integer, default=1, nullable=False)
    
    # Content Fields
    headline = Column(String(200), nullable=False)
    subheadline = Column(Text, nullable=True)
    cta_text = Column(String(100), default="Get Started")
    features = Column(Text, nullable=True)  # JSON string
    testimonials = Column(Text, nullable=True)  # JSON string
    about_section = Column(Text, nullable=True)
    
    # SEO Fields
    meta_title = Column(String(60), nullable=True)
    meta_description = Column(String(160), nullable=True)
    keywords = Column(Text, nullable=True)  # JSON array
    og_title = Column(String(100), nullable=True)
    og_description = Column(String(200), nullable=True)
    
    # Design Fields
    theme = Column(String(50), default="modern")
    primary_color = Column(String(7), default="#3B82F6")  # Hex color
    secondary_color = Column(String(7), default="#1E40AF")
    
    # File Paths
    html_path = Column(String(255), nullable=True)
    css_path = Column(String(255), nullable=True)
    
    # Metadata
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
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
