"""
API integration tests for all endpoints.
"""
import pytest
import asyncio
from fastapi.testclient import TestClient

# Add parent directory to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.database import init_db


# Create test client
client = TestClient(app)


# Initialize database before tests
def setup_test_database():
    """Set up test database."""
    print("\n🔧 Setting up test database...")
    init_db()
    print("✅ Database ready")


def test_root_endpoint():
    """Test root endpoint."""
    print("\n🧪 Testing Root Endpoint...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"
    print("✅ Root endpoint working")


def test_health_check():
    """Test health check endpoint."""
    print("\n🧪 Testing Health Check...")
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    print("✅ Health check passed")


def test_detailed_health_check():
    """Test detailed health check."""
    print("\n🧪 Testing Detailed Health Check...")
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "checks" in data
    assert "database" in data["checks"]
    assert data["checks"]["database"]["status"] == "healthy"
    print("✅ Detailed health check passed")


def test_version_info():
    """Test version info endpoint."""
    print("\n🧪 Testing Version Info...")
    response = client.get("/api/v1/health/version")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0.0"
    assert data["api_version"] == "v1"
    print("✅ Version info retrieved")


def test_create_business():
    """Test creating a business."""
    print("\n🧪 Testing Business Creation...")
    business_data = {
        "name": "Test Business API",
        "industry": "Technology",
        "target_audience": "Developers",
        "tone": "Professional",
        "goal": "Generate leads",
        "unique_value_proposition": "Best in class solutions"
    }
    
    response = client.post("/api/v1/businesses/", json=business_data)
    print(f"Response status: {response.status_code}")
    if response.status_code != 201:
        print(f"Response content: {response.json()}")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == business_data["name"]
    assert data["industry"] == business_data["industry"]
    assert "id" in data
    print(f"✅ Business created with ID: {data['id']}")
    return data["id"]


def test_list_businesses():
    """Test listing businesses."""
    print("\n🧪 Testing Business Listing...")
    response = client.get("/api/v1/businesses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    print(f"✅ Found {len(data)} businesses")


def test_get_business():
    """Test getting a specific business."""
    print("\n🧪 Testing Get Business...")
    # Create a business first
    business_id = test_create_business()
    
    # Get the business
    response = client.get(f"/api/v1/businesses/{business_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == business_id
    print(f"✅ Retrieved business {business_id}")


def test_update_business():
    """Test updating a business."""
    print("\n🧪 Testing Business Update...")
    # Create a business first
    business_id = test_create_business()
    
    # Update the business
    update_data = {
        "name": "Updated Test Business",
        "tone": "friendly"  # tone is normalized to lowercase by the schema
    }
    
    response = client.put(f"/api/v1/businesses/{business_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["tone"] == update_data["tone"]
    print("✅ Business updated successfully")


def test_business_count():
    """Test business count endpoint."""
    print("\n🧪 Testing Business Count...")
    response = client.get("/api/v1/businesses/stats/count")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert data["count"] >= 0
    print(f"✅ Total businesses: {data['count']}")


def test_generate_landing_page():
    """Test landing page generation."""
    print("\n🧪 Testing Landing Page Generation...")
    # Create a business first
    business_data = {
        "name": "AI Test Company",
        "industry": "Artificial Intelligence",
        "target_audience": "Tech companies",
        "tone": "Professional and innovative",
        "goal": "Generate leads",
        "unique_value_proposition": "Cutting-edge AI solutions"
    }
    
    business_response = client.post("/api/v1/businesses/", json=business_data)
    business_id = business_response.json()["id"]
    
    # Generate landing page
    customization = {
        "theme": "modern",
        "primary_color": "#3B82F6",
        "secondary_color": "#10B981",
        "num_features": 3,
        "num_testimonials": 2,
        "include_features": True,
        "include_testimonials": True
    }
    
    print(f"🤖 Generating landing page for business {business_id}...")
    response = client.post(
        f"/api/v1/landing-pages/generate/{business_id}",
        json=customization
    )
    
    # This might take a while due to AI generation
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["business_id"] == business_id
    assert data["headline"] is not None
    assert len(data["features"]) == 3
    assert len(data["testimonials"]) == 2
    print(f"✅ Landing page generated (ID: {data['id']})")
    print(f"   Headline: {data['headline']}")
    print(f"   Features: {len(data['features'])}")
    print(f"   Testimonials: {len(data['testimonials'])}")
    return data["id"]


def test_list_landing_pages():
    """Test listing landing pages."""
    print("\n🧪 Testing Landing Page Listing...")
    response = client.get("/api/v1/landing-pages/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"✅ Found {len(data)} landing pages")


def test_get_landing_page():
    """Test getting a specific landing page."""
    print("\n🧪 Testing Get Landing Page...")
    # Generate a landing page first
    page_id = test_generate_landing_page()
    
    # Get the landing page
    response = client.get(f"/api/v1/landing-pages/{page_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == page_id
    print(f"✅ Retrieved landing page {page_id}")


def test_publish_landing_page():
    """Test publishing a landing page."""
    print("\n🧪 Testing Landing Page Publish...")
    # Generate a landing page first
    page_id = test_generate_landing_page()
    
    # Publish it
    response = client.post(f"/api/v1/landing-pages/{page_id}/publish")
    assert response.status_code == 200
    data = response.json()
    assert data["is_published"] is True
    print("✅ Landing page published")


def test_unpublish_landing_page():
    """Test unpublishing a landing page."""
    print("\n🧪 Testing Landing Page Unpublish...")
    # Generate and publish a landing page first
    page_id = test_generate_landing_page()
    client.post(f"/api/v1/landing-pages/{page_id}/publish")
    
    # Unpublish it
    response = client.post(f"/api/v1/landing-pages/{page_id}/unpublish")
    assert response.status_code == 200
    data = response.json()
    assert data["is_published"] is False
    print("✅ Landing page unpublished")


def test_track_page_view():
    """Test tracking page views."""
    print("\n🧪 Testing Page View Tracking...")
    # Generate a landing page first
    page_id = test_generate_landing_page()
    
    # Track a view
    response = client.post(f"/api/v1/landing-pages/{page_id}/view")
    assert response.status_code == 204
    
    # Verify view count increased
    page_response = client.get(f"/api/v1/landing-pages/{page_id}")
    data = page_response.json()
    assert data["view_count"] >= 1
    print(f"✅ View tracked (count: {data['view_count']})")


def test_landing_page_count():
    """Test landing page count endpoint."""
    print("\n🧪 Testing Landing Page Count...")
    response = client.get("/api/v1/landing-pages/stats/count")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    print(f"✅ Total landing pages: {data['count']}")


def test_delete_business():
    """Test deleting a business."""
    print("\n🧪 Testing Business Deletion...")
    # Create a business first
    business_id = test_create_business()
    
    # Delete it
    response = client.delete(f"/api/v1/businesses/{business_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/businesses/{business_id}")
    assert get_response.status_code == 404
    print("✅ Business deleted successfully")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API INTEGRATION TESTS")
    print("=" * 60)
    
    # Run tests manually
    setup_test_database()
    
    test_root_endpoint()
    test_health_check()
    test_detailed_health_check()
    test_version_info()
    
    test_create_business()
    test_list_businesses()
    test_get_business()
    test_update_business()
    test_business_count()
    
    print("\n⚠️  Note: AI generation tests require API keys and may take time...")
    # Uncomment to run AI tests:
    # test_generate_landing_page()
    # test_list_landing_pages()
    # test_get_landing_page()
    # test_publish_landing_page()
    # test_unpublish_landing_page()
    # test_track_page_view()
    # test_landing_page_count()
    
    test_delete_business()
    
    print("\n" + "=" * 60)
    print("✅ API TESTS COMPLETED!")
    print("=" * 60)
