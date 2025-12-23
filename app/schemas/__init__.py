"""
Pydantic schemas package for request/response validation
"""

from .business import BusinessInput, BusinessOutput, BusinessUpdate
from .landing_page import (
    PageCustomization,
    PageGenerationRequest,
    PageOutput,
    PageListOutput,
    PageUpdate,
    PageStats,
    FeatureItem,
    TestimonialItem
)

__all__ = [
    # Business schemas
    "BusinessInput",
    "BusinessOutput",
    "BusinessUpdate",
    # Landing page schemas
    "PageCustomization",
    "PageGenerationRequest",
    "PageOutput",
    "PageListOutput",
    "PageUpdate",
    "PageStats",
    "FeatureItem",
    "TestimonialItem",
]
