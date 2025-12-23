"""
Unit tests for Landing Page model and CRUD operations.
"""
import pytest
import json
from app.crud import landing_page as page_crud
from app.schemas.landing_page import PageCustomization, PageUpdate
from app.models.landing_page import LandingPage

@pytest.mark.unit
class TestLandingPageModel:
    """Test LandingPage model."""
    
    def test_create_landing_page(self, test_db, sample_business):
        """Test creating a landing page."""
        page = LandingPage(
            business_id=sample_business.id,
            headline="Test Headline",
            subheadline="Test Subheadline",
            cta_text="Click Here",
            features='["Feature 1", "Feature 2"]',
            testimonials='[]',
            theme="modern",
            primary_color="#000000",
            secondary_color="#FFFFFF"
        )
        test_db.add(page)
        test_db.commit()
        test_db.refresh(page)
        
        assert page.id is not None
        assert page.business_id == sample_business.id
        assert page.headline == "Test Headline"
        assert page.is_published is False
        assert page.view_count == 0
    
    def test_landing_page_features_json(self, sample_landing_page):
        """Test features are stored as JSON."""
        features = json.loads(sample_landing_page.features)
        assert isinstance(features, list)
        assert len(features) == 3
    
    def test_landing_page_get_features(self, sample_landing_page):
        """Test get_features method."""
        features = sample_landing_page.get_features()
        assert isinstance(features, list)
        assert len(features) == 3
    
    def test_landing_page_get_testimonials(self, sample_landing_page):
        """Test get_testimonials method."""
        testimonials = sample_landing_page.get_testimonials()
        assert isinstance(testimonials, list)
        assert len(testimonials) == 1
        assert testimonials[0]["name"] == "John Doe"
    
    def test_landing_page_get_keywords(self, sample_landing_page):
        """Test get_keywords method."""
        keywords = sample_landing_page.get_keywords()
        assert isinstance(keywords, list)
        assert "business" in keywords

@pytest.mark.unit
class TestLandingPageCRUD:
    """Test Landing Page CRUD operations."""
    
    def test_get_landing_page(self, test_db, sample_landing_page):
        """Test getting a landing page by ID."""
        page = page_crud.get_landing_page(test_db, sample_landing_page.id)
        
        assert page is not None
        assert page.id == sample_landing_page.id
        assert page.headline == sample_landing_page.headline
    
    def test_get_landing_page_not_found(self, test_db):
        """Test getting non-existent landing page."""
        page = page_crud.get_landing_page(test_db, 99999)
        assert page is None
    
    def test_get_landing_pages_empty(self, test_db):
        """Test getting landing pages when none exist."""
        pages = page_crud.get_landing_pages(test_db)
        assert pages == []
    
    def test_get_landing_pages(self, test_db, sample_landing_page):
        """Test getting all landing pages."""
        pages = page_crud.get_landing_pages(test_db)
        
        assert len(pages) >= 1
        assert any(p.id == sample_landing_page.id for p in pages)
    
    def test_get_landing_pages_by_business(self, test_db, sample_landing_page):
        """Test getting landing pages by business ID."""
        pages = page_crud.get_landing_pages(
            test_db, 
            business_id=sample_landing_page.business_id
        )
        
        assert len(pages) >= 1
        assert all(p.business_id == sample_landing_page.business_id for p in pages)
    
    def test_get_landing_pages_published_only(self, test_db, sample_landing_page):
        """Test getting only published pages."""
        # Initially no published pages
        published = page_crud.get_landing_pages(test_db, published_only=True)
        assert len(published) == 0
        
        # Publish the page
        sample_landing_page.is_published = True
        test_db.commit()
        
        published = page_crud.get_landing_pages(test_db, published_only=True)
        assert len(published) == 1
    
    def test_get_landing_pages_pagination(self, test_db, sample_business):
        """Test landing page pagination."""
        # Create multiple pages
        for i in range(5):
            page = LandingPage(
                business_id=sample_business.id,
                headline=f"Headline {i}",
                subheadline=f"Subheadline {i}",
                cta_text="CTA",
                features='[]',
                testimonials='[]',
                theme="modern"
            )
            test_db.add(page)
        test_db.commit()
        
        page1 = page_crud.get_landing_pages(test_db, skip=0, limit=2)
        page2 = page_crud.get_landing_pages(test_db, skip=2, limit=2)
        
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].id != page2[0].id
    
    def test_update_landing_page(self, test_db, sample_landing_page):
        """Test updating a landing page."""
        update_data = PageUpdate(
            headline="New Headline",
            subheadline="New Subheadline",
            primary_color="#FF0000"
        )
        
        updated = page_crud.update_landing_page(
            test_db,
            sample_landing_page.id,
            update_data
        )
        
        assert updated.headline == "New Headline"
        assert updated.subheadline == "New Subheadline"
        assert updated.primary_color == "#FF0000"
        assert updated.cta_text == sample_landing_page.cta_text  # Unchanged
    
    def test_update_landing_page_not_found(self, test_db):
        """Test updating non-existent landing page."""
        update_data = PageUpdate(headline="Updated Test Headline")
        updated = page_crud.update_landing_page(test_db, 99999, update_data)
        assert updated is None
    
    def test_publish_landing_page(self, test_db, sample_landing_page):
        """Test publishing a landing page."""
        assert sample_landing_page.is_published is False
        
        published = page_crud.publish_landing_page(test_db, sample_landing_page.id)
        
        assert published.is_published is True
    
    def test_unpublish_landing_page(self, test_db, sample_landing_page):
        """Test unpublishing a landing page."""
        # First publish
        sample_landing_page.is_published = True
        test_db.commit()
        
        unpublished = page_crud.unpublish_landing_page(test_db, sample_landing_page.id)
        
        assert unpublished.is_published is False
    
    def test_increment_view_count(self, test_db, sample_landing_page):
        """Test incrementing view count."""
        initial_count = sample_landing_page.view_count
        
        page_crud.increment_view_count(test_db, sample_landing_page.id)
        test_db.refresh(sample_landing_page)
        
        assert sample_landing_page.view_count == initial_count + 1
    
    def test_increment_view_count_multiple(self, test_db, sample_landing_page):
        """Test incrementing view count multiple times."""
        for _ in range(5):
            page_crud.increment_view_count(test_db, sample_landing_page.id)
        
        test_db.refresh(sample_landing_page)
        assert sample_landing_page.view_count == 5
    
    def test_delete_landing_page(self, test_db, sample_landing_page):
        """Test deleting a landing page."""
        page_id = sample_landing_page.id
        
        result = page_crud.delete_landing_page(test_db, page_id)
        assert result is True
        
        # Verify deletion
        page = page_crud.get_landing_page(test_db, page_id)
        assert page is None
    
    def test_delete_landing_page_not_found(self, test_db):
        """Test deleting non-existent landing page."""
        result = page_crud.delete_landing_page(test_db, 99999)
        assert result is False
    
    def test_count_landing_pages(self, test_db, sample_landing_page):
        """Test counting landing pages."""
        count = page_crud.count_landing_pages(test_db)
        assert count >= 1
    
    def test_count_landing_pages_by_business(self, test_db, sample_landing_page):
        """Test counting landing pages by business."""
        count = page_crud.count_landing_pages(
            test_db,
            business_id=sample_landing_page.business_id
        )
        assert count >= 1
    
    def test_count_landing_pages_empty(self, test_db):
        """Test counting when no pages exist."""
        count = page_crud.count_landing_pages(test_db)
        assert count == 0
