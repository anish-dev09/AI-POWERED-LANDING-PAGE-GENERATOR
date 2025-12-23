"""
Test fixtures and configuration for pytest.
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.business import Business
from app.models.landing_page import LandingPage

# Test database URL - using in-memory database to avoid file locking issues on Windows
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    # Create test database (in-memory)
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)
        # Dispose engine to close all connections
        engine.dispose()

@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with the test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_business(test_db):
    """Create a sample business for testing."""
    business = Business(
        name="TechStart Solutions",
        industry="SaaS",
        target_audience="Small business owners",
        unique_value_proposition="All-in-one business management platform",
        tone="professional",
        goal="lead_generation"
    )
    test_db.add(business)
    test_db.commit()
    test_db.refresh(business)
    return business

@pytest.fixture
def sample_landing_page(test_db, sample_business):
    """Create a sample landing page for testing."""
    page = LandingPage(
        business_id=sample_business.id,
        headline="Transform Your Business Today",
        subheadline="The complete solution for modern entrepreneurs",
        cta_text="Get Started Free",
        features='["Feature 1", "Feature 2", "Feature 3"]',
        testimonials='[{"name": "John Doe", "role": "CEO", "content": "Great product!"}]',
        theme="modern",
        primary_color="#8B5CF6",
        secondary_color="#EC4899",
        keywords='["business", "management", "saas"]',
        meta_title="TechStart Solutions - Business Management",
        meta_description="Transform your business with our all-in-one platform",
        is_published=False,
        view_count=0
    )
    test_db.add(page)
    test_db.commit()
    test_db.refresh(page)
    return page

@pytest.fixture
def multiple_businesses(test_db):
    """Create multiple businesses for testing."""
    businesses = [
        Business(
            name=f"Business {i}",
            industry="Technology" if i % 2 == 0 else "E-commerce",
            target_audience="Developers" if i % 2 == 0 else "Shoppers",
            unique_value_proposition=f"Value proposition {i}",
            tone="professional",
            goal="lead_generation"
        )
        for i in range(1, 6)
    ]
    test_db.add_all(businesses)
    test_db.commit()
    for business in businesses:
        test_db.refresh(business)
    return businesses

@pytest.fixture
def mock_ai_response():
    """Mock AI API response for testing."""
    return {
        "headline": "Test Headline",
        "subheadline": "Test Subheadline",
        "cta_text": "Get Started",
        "features": ["Feature 1", "Feature 2", "Feature 3"],
        "testimonials": [
            {
                "name": "Jane Smith",
                "role": "Marketing Director",
                "content": "This product changed everything!",
                "rating": 5
            }
        ],
        "keywords": ["test", "sample", "demo"],
        "meta_title": "Test Page Title",
        "meta_description": "Test page description"
    }
