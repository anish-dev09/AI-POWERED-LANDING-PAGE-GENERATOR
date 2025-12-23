"""
Business model - stores business information
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Business(Base):
    """
    Business model representing a company/organization
    that wants to generate landing pages.
    
    Attributes:
        id: Primary key
        name: Business name
        industry: Business industry/sector
        target_audience: Description of target audience
        tone: Communication tone (professional, friendly, bold, elegant)
        goal: Primary goal of the landing page
        unique_value_proposition: What makes the business unique
        additional_info: Any additional context
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
        
    Relationships:
        landing_pages: All landing pages generated for this business
    """
    
    __tablename__ = "businesses"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Business Information
    name = Column(String(100), nullable=False, index=True)
    industry = Column(String(50), nullable=False)
    target_audience = Column(String(200), nullable=False)
    tone = Column(String(20), default="professional")  # professional, friendly, bold, elegant
    goal = Column(Text, nullable=False)
    unique_value_proposition = Column(Text, nullable=True)
    additional_info = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    landing_pages = relationship(
        "LandingPage",
        back_populates="business",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<Business(id={self.id}, name='{self.name}', industry='{self.industry}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "target_audience": self.target_audience,
            "tone": self.tone,
            "goal": self.goal,
            "unique_value_proposition": self.unique_value_proposition,
            "additional_info": self.additional_info,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
