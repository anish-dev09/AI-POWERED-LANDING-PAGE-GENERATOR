"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestBusinessAPI:
    """Test Business API endpoints."""
    
    def test_create_business(self, client):
        """Test creating a business via API."""
        response = client.post("/api/v1/businesses/", json={
            "name": "API Test Company",
            "industry": "Technology",
            "target_audience": "Developers",
            "unique_value_proposition": "Best tools ever",
            "tone": "professional",
            "goal": "lead_generation"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "API Test Company"
        assert data["industry"] == "Technology"
        assert "id" in data
    
    def test_create_business_missing_fields(self, client):
        """Test creating business with missing required fields."""
        response = client.post("/api/v1/businesses/", json={
            "name": "Incomplete Business"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_get_businesses_empty(self, client):
        """Test getting businesses when none exist."""
        response = client.get("/api/v1/businesses/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_businesses(self, client, sample_business):
        """Test getting all businesses."""
        response = client.get("/api/v1/businesses/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(b["id"] == sample_business.id for b in data)
    
    def test_get_business_by_id(self, client, sample_business):
        """Test getting a specific business."""
        response = client.get(f"/api/v1/businesses/{sample_business.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_business.id
        assert data["name"] == sample_business.name
    
    def test_get_business_not_found(self, client):
        """Test getting non-existent business."""
        response = client.get("/api/v1/businesses/99999")
        
        assert response.status_code == 404
    
    def test_update_business(self, client, sample_business):
        """Test updating a business."""
        response = client.put(
            f"/api/v1/businesses/{sample_business.id}",
            json={"name": "Updated Business Name"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Business Name"
    
    def test_update_business_not_found(self, client):
        """Test updating non-existent business."""
        response = client.put(
            "/api/v1/businesses/99999",
            json={"name": "Test"}
        )
        
        assert response.status_code == 404
    
    def test_delete_business(self, client, sample_business):
        """Test deleting a business."""
        business_id = sample_business.id
        
        response = client.delete(f"/api/v1/businesses/{business_id}")
        
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/businesses/{business_id}")
        assert get_response.status_code == 404
    
    def test_delete_business_not_found(self, client):
        """Test deleting non-existent business."""
        response = client.delete("/api/v1/businesses/99999")
        
        assert response.status_code == 404
    
    def test_count_businesses(self, client, multiple_businesses):
        """Test counting businesses."""
        response = client.get("/api/v1/businesses/stats/count")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 5
    
    def test_search_businesses(self, client, multiple_businesses):
        """Test searching businesses."""
        response = client.get("/api/v1/businesses/?search=Technology")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_pagination(self, client, multiple_businesses):
        """Test business pagination."""
        response = client.get("/api/v1/businesses/?skip=0&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

@pytest.mark.integration
class TestLandingPageAPI:
    """Test Landing Page API endpoints."""
    
    def test_get_landing_pages_empty(self, client):
        """Test getting landing pages when none exist."""
        response = client.get("/api/v1/landing-pages/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_landing_pages(self, client, sample_landing_page):
        """Test getting all landing pages."""
        response = client.get("/api/v1/landing-pages/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_get_landing_page_by_id(self, client, sample_landing_page):
        """Test getting a specific landing page."""
        response = client.get(f"/api/v1/landing-pages/{sample_landing_page.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_landing_page.id
        assert data["headline"] == sample_landing_page.headline
        assert "features" in data
        assert "testimonials" in data
    
    def test_get_landing_page_not_found(self, client):
        """Test getting non-existent landing page."""
        response = client.get("/api/v1/landing-pages/99999")
        
        assert response.status_code == 404
    
    def test_update_landing_page(self, client, sample_landing_page):
        """Test updating a landing page."""
        response = client.put(
            f"/api/v1/landing-pages/{sample_landing_page.id}",
            json={"headline": "Updated Headline"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["headline"] == "Updated Headline"
    
    def test_publish_landing_page(self, client, sample_landing_page):
        """Test publishing a landing page."""
        response = client.post(f"/api/v1/landing-pages/{sample_landing_page.id}/publish")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_published"] is True
    
    def test_unpublish_landing_page(self, client, sample_landing_page):
        """Test unpublishing a landing page."""
        # First publish
        client.post(f"/api/v1/landing-pages/{sample_landing_page.id}/publish")
        
        # Then unpublish
        response = client.post(f"/api/v1/landing-pages/{sample_landing_page.id}/unpublish")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_published"] is False
    
    def test_track_view(self, client, sample_landing_page):
        """Test tracking page view."""
        response = client.post(f"/api/v1/landing-pages/{sample_landing_page.id}/view")
        
        assert response.status_code == 204
    
    def test_delete_landing_page(self, client, sample_landing_page):
        """Test deleting a landing page."""
        page_id = sample_landing_page.id
        
        response = client.delete(f"/api/v1/landing-pages/{page_id}")
        
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/landing-pages/{page_id}")
        assert get_response.status_code == 404
    
    def test_count_landing_pages(self, client, sample_landing_page):
        """Test counting landing pages."""
        response = client.get("/api/v1/landing-pages/stats/count")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 1
    
    def test_filter_by_business(self, client, sample_landing_page):
        """Test filtering landing pages by business."""
        response = client.get(
            f"/api/v1/landing-pages/?business_id={sample_landing_page.business_id}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(p["business_id"] == sample_landing_page.business_id for p in data)
    
    def test_filter_published_only(self, client, sample_landing_page):
        """Test filtering for published pages only."""
        response = client.get("/api/v1/landing-pages/?published_only=true")
        
        assert response.status_code == 200
        data = response.json()
        assert all(p["is_published"] for p in data)

@pytest.mark.integration
class TestHealthAPI:
    """Test Health Check API endpoints."""
    
    def test_health_check(self, client):
        """Test basic health check."""
        response = client.get("/api/v1/health/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_detailed_health_check(self, client):
        """Test detailed health check."""
        response = client.get("/api/v1/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
        assert "statistics" in data
    
    def test_version_info(self, client):
        """Test version info endpoint."""
        response = client.get("/api/v1/health/version")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "api_version" in data

@pytest.mark.integration
class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
