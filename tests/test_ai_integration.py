"""
Test script to verify AI integration and content generation.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, init_db
from app.crud.business import create_business
from app.schemas.business import BusinessInput
from app.schemas.landing_page import PageCustomization
from app.services.landing_page_service import get_landing_page_service


async def test_ai_content_generation():
    """Test AI content generation end-to-end."""
    
    print("=" * 60)
    print("🧪 Testing AI Integration & Content Generation")
    print("=" * 60)
    
    # Initialize database
    print("\n1️⃣ Initializing database...")
    init_db()
    print("✓ Database initialized")
    
    # Create a test business
    print("\n2️⃣ Creating test business...")
    db = SessionLocal()
    
    try:
        business_data = BusinessInput(
            name="TechStart Solutions",
            industry="Technology Consulting",
            target_audience="Small to medium businesses looking to modernize their IT infrastructure",
            tone="professional",
            goal="Generate qualified leads for IT consulting services and increase brand awareness",
            unique_value_proposition="20+ years combined experience with 98% client satisfaction rate",
            additional_info="Focus on cloud migration and cybersecurity solutions"
        )
        
        business = create_business(db, business_data)
        print(f"✓ Business created: {business.name} (ID: {business.id})")
        
        # Generate landing page
        print("\n3️⃣ Generating landing page content using AI...")
        print("   This may take 10-20 seconds...")
        
        customization = PageCustomization(
            theme="modern",
            primary_color="#3B82F6",
            secondary_color="#10B981",
            num_features=3,
            num_testimonials=2
        )
        
        service = get_landing_page_service()
        page = await service.generate_landing_page(
            db=db,
            business_id=business.id,
            customization=customization
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("✅ LANDING PAGE GENERATED SUCCESSFULLY!")
        print("=" * 60)
        
        print(f"\n📝 HEADLINE:")
        print(f"   {page['headline']}")
        
        print(f"\n📄 SUBHEADLINE:")
        print(f"   {page['subheadline']}")
        
        print(f"\n🎯 CTA:")
        print(f"   {page['cta_text']}")
        
        print(f"\n⭐ FEATURES ({len(page['features'])}):")
        for i, feature in enumerate(page['features'], 1):
            print(f"   {i}. {feature.get('icon', '•')} {feature.get('title', 'N/A')}")
            print(f"      {feature.get('description', 'N/A')}")
        
        print(f"\n💬 TESTIMONIALS ({len(page['testimonials'])}):")
        for i, testimonial in enumerate(page['testimonials'], 1):
            print(f"   {i}. {testimonial.get('name', 'N/A')} - {testimonial.get('role', 'N/A')} at {testimonial.get('company', 'N/A')}")
            print(f"      \"{testimonial.get('content', 'N/A')}\"")
            print(f"      Rating: {'⭐' * testimonial.get('rating', 0)}")
        
        print(f"\n🔍 SEO METADATA:")
        print(f"   Meta Title: {page['meta_title']}")
        print(f"   Meta Description: {page['meta_description']}")
        print(f"   Keywords: {', '.join(page['keywords'][:5])}")
        
        print(f"\n🎨 DESIGN:")
        print(f"   Theme: {page['theme']}")
        print(f"   Primary Color: {page['primary_color']}")
        print(f"   Secondary Color: {page['secondary_color']}")
        
        print(f"\n💾 DATABASE:")
        print(f"   Page ID: {page['id']}")
        print(f"   Business ID: {page['business_id']}")
        print(f"   Created: {page['created_at']}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()
    
    return True


if __name__ == "__main__":
    print("\n" + "🚀 Starting AI Integration Test..." + "\n")
    
    # Run the async test
    success = asyncio.run(test_ai_content_generation())
    
    if success:
        print("\n✨ Phase 3 AI Integration is working perfectly! ✨\n")
        sys.exit(0)
    else:
        print("\n💥 Tests failed. Please check the errors above.\n")
        sys.exit(1)
