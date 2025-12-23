"""
Business-related Pydantic schemas for request/response validation.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class BusinessInput(BaseModel):
    """Schema for creating a new business."""
    name: str = Field(..., min_length=2, max_length=100, description="Business name")
    industry: str = Field(..., min_length=2, max_length=100, description="Industry/sector")
    target_audience: str = Field(..., min_length=5, max_length=500, description="Target audience description")
    tone: str = Field(default="professional", max_length=50, description="Communication tone (e.g., professional, casual, friendly)")
    goal: str = Field(..., min_length=10, max_length=1000, description="Primary business goal for the landing page")
    unique_value_proposition: Optional[str] = Field(None, max_length=500, description="What makes this business unique")
    additional_info: Optional[str] = Field(None, max_length=2000, description="Any additional context or requirements")

    @field_validator('tone')
    @classmethod
    def validate_tone(cls, v: str) -> str:
        """Validate tone is one of the allowed values."""
        allowed_tones = ['professional', 'casual', 'friendly', 'formal', 'conversational', 'authoritative', 'playful']
        if v.lower() not in allowed_tones:
            raise ValueError(f'Tone must be one of: {", ".join(allowed_tones)}')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TechStart Solutions",
                "industry": "Technology Consulting",
                "target_audience": "Small to medium businesses looking to modernize their IT infrastructure",
                "tone": "professional",
                "goal": "Generate qualified leads for IT consulting services and increase brand awareness",
                "unique_value_proposition": "20+ years combined experience with 98% client satisfaction rate",
                "additional_info": "Focus on cloud migration and cybersecurity"
            }
        }


class BusinessOutput(BaseModel):
    """Schema for business response."""
    id: int
    name: str
    industry: str
    target_audience: str
    tone: str
    goal: str
    unique_value_proposition: Optional[str] = None
    additional_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2 (replaces orm_mode)


# Aliases for API compatibility
BusinessCreate = BusinessInput
BusinessResponse = BusinessOutput


class BusinessUpdate(BaseModel):
    """Schema for updating business information."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    industry: Optional[str] = Field(None, min_length=2, max_length=100)
    target_audience: Optional[str] = Field(None, min_length=5, max_length=500)
    tone: Optional[str] = Field(None, max_length=50)
    goal: Optional[str] = Field(None, min_length=10, max_length=1000)
    unique_value_proposition: Optional[str] = Field(None, max_length=500)
    additional_info: Optional[str] = Field(None, max_length=2000)

    @field_validator('tone')
    @classmethod
    def validate_tone(cls, v: Optional[str]) -> Optional[str]:
        """Validate tone if provided."""
        if v is None:
            return v
        allowed_tones = ['professional', 'casual', 'friendly', 'formal', 'conversational', 'authoritative', 'playful']
        if v.lower() not in allowed_tones:
            raise ValueError(f'Tone must be one of: {", ".join(allowed_tones)}')
        return v.lower()
