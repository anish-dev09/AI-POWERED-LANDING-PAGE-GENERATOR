"""
Unit tests for Business model and CRUD operations.
"""
import pytest
from app.crud import business as business_crud
from app.schemas.business import BusinessInput, BusinessUpdate
from app.models.business import Business

@pytest.mark.unit
class TestBusinessModel:
    """Test Business model."""
    
    def test_create_business(self, test_db):
        """Test creating a business."""
        business = Business(
            name="Test Company",
            industry="Technology",
            target_audience="Developers",
            unique_value_proposition="Best tools",
            tone="professional",
            goal="lead_generation"
        )
        test_db.add(business)
        test_db.commit()
        test_db.refresh(business)
        
        assert business.id is not None
        assert business.name == "Test Company"
        assert business.industry == "Technology"
        assert business.created_at is not None
        assert business.updated_at is not None
    
    def test_business_string_representation(self, sample_business):
        """Test business __repr__ method."""
        assert "TechStart Solutions" in repr(sample_business)

@pytest.mark.unit
class TestBusinessCRUD:
    """Test Business CRUD operations."""
    
    def test_create_business_crud(self, test_db):
        """Test creating business via CRUD."""
        business_data = BusinessInput(
            name="New Business",
            industry="E-commerce",
            target_audience="Online shoppers",
            unique_value_proposition="Fast delivery service",
            tone="friendly",
            goal="Increase sales and customer base"
        )
        
        business = business_crud.create_business(test_db, business_data)
        
        assert business.id is not None
        assert business.name == "New Business"
        assert business.industry == "E-commerce"
        assert business.tone == "friendly"
    
    def test_get_business(self, test_db, sample_business):
        """Test getting a business by ID."""
        business = business_crud.get_business(test_db, sample_business.id)
        
        assert business is not None
        assert business.id == sample_business.id
        assert business.name == sample_business.name
    
    def test_get_business_not_found(self, test_db):
        """Test getting non-existent business."""
        business = business_crud.get_business(test_db, 99999)
        assert business is None
    
    def test_get_businesses_empty(self, test_db):
        """Test getting businesses when none exist."""
        businesses = business_crud.get_businesses(test_db)
        assert businesses == []
    
    def test_get_businesses(self, test_db, multiple_businesses):
        """Test getting all businesses."""
        businesses = business_crud.get_businesses(test_db)
        
        assert len(businesses) == 5
        assert all(isinstance(b, Business) for b in businesses)
    
    def test_get_businesses_with_pagination(self, test_db, multiple_businesses):
        """Test getting businesses with pagination."""
        page1 = business_crud.get_businesses(test_db, skip=0, limit=2)
        page2 = business_crud.get_businesses(test_db, skip=2, limit=2)
        
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].id != page2[0].id
    
    def test_search_businesses(self, test_db, multiple_businesses):
        """Test searching businesses."""
        # Search by industry
        tech_businesses = business_crud.get_businesses(test_db, search="Technology")
        assert len(tech_businesses) >= 2
        
        # Search by name
        business_1 = business_crud.get_businesses(test_db, search="Business 1")
        assert len(business_1) == 1
    
    def test_update_business(self, test_db, sample_business):
        """Test updating a business."""
        update_data = BusinessUpdate(
            name="Updated Name",
            industry="New Industry"
        )
        
        updated = business_crud.update_business(test_db, sample_business.id, update_data)
        
        assert updated.name == "Updated Name"
        assert updated.industry == "New Industry"
        assert updated.target_audience == sample_business.target_audience  # Unchanged
    
    def test_update_business_partial(self, test_db, sample_business):
        """Test partial update of business."""
        update_data = BusinessUpdate(tone="casual")
        
        updated = business_crud.update_business(test_db, sample_business.id, update_data)
        
        assert updated.tone == "casual"
        assert updated.name == sample_business.name  # Unchanged
    
    def test_update_business_not_found(self, test_db):
        """Test updating non-existent business."""
        update_data = BusinessUpdate(name="Test")
        updated = business_crud.update_business(test_db, 99999, update_data)
        assert updated is None
    
    def test_delete_business(self, test_db, sample_business):
        """Test deleting a business."""
        business_id = sample_business.id
        
        result = business_crud.delete_business(test_db, business_id)
        assert result is True
        
        # Verify deletion
        business = business_crud.get_business(test_db, business_id)
        assert business is None
    
    def test_delete_business_not_found(self, test_db):
        """Test deleting non-existent business."""
        result = business_crud.delete_business(test_db, 99999)
        assert result is False
    
    def test_count_businesses(self, test_db, multiple_businesses):
        """Test counting businesses."""
        count = business_crud.count_businesses(test_db)
        assert count == 5
    
    def test_count_businesses_empty(self, test_db):
        """Test counting when no businesses exist."""
        count = business_crud.count_businesses(test_db)
        assert count == 0
