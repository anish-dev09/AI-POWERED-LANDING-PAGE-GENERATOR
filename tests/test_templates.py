"""
Integration tests for HTML/CSS template rendering.
Tests the template service and CSS generator with sample data.
"""

import pytest
import os
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.business import Business
from app.models.landing_page import LandingPage
from app.services.template_service import TemplateService, get_template_service, render_landing_page_html
from app.services.css_generator import CSSGenerator, get_css_generator, generate_landing_page_css


def create_mock_business() -> Business:
    """Create a mock Business instance for testing."""
    business = Business()
    business.id = 1
    business.name = "TechStart Solutions"
    business.industry = "Technology Consulting"
    business.target_audience = "Small to medium businesses"
    business.tone = "Professional and approachable"
    business.goal = "Generate leads"
    business.unique_value_proposition = "Modernizing businesses through innovative IT solutions"
    business.additional_info = "10+ years of experience"
    business.created_at = datetime.now()
    business.updated_at = datetime.now()
    return business


def create_mock_landing_page() -> LandingPage:
    """Create a mock LandingPage instance for testing."""
    landing_page = LandingPage()
    landing_page.id = 1
    landing_page.business_id = 1
    landing_page.version = 1
    landing_page.headline = "Transform Your Business with Modern IT Solutions"
    landing_page.subheadline = "Expert consulting to modernize your infrastructure, enhance security, and accelerate growth"
    landing_page.cta_text = "Get Your Free Consultation"
    
    # Features (JSON string)
    features = [
        {
            "title": "Cloud Migration",
            "description": "Seamlessly transition to cloud infrastructure with zero downtime",
            "icon": "☁️"
        },
        {
            "title": "Cybersecurity",
            "description": "Protect your business with enterprise-grade security solutions",
            "icon": "🔒"
        },
        {
            "title": "IT Strategy",
            "description": "Strategic planning to align technology with business goals",
            "icon": "💡"
        }
    ]
    landing_page.features = json.dumps(features)
    
    # Testimonials (JSON string)
    testimonials = [
        {
            "name": "Sarah Chen",
            "title": "CTO",
            "company": "InnovateCo",
            "text": "TechStart transformed our IT infrastructure. We're now more efficient and secure than ever.",
            "rating": 5
        },
        {
            "name": "Michael Rodriguez",
            "title": "CEO",
            "company": "GrowthStart",
            "text": "The best IT consulting partner we've worked with. Highly recommended!",
            "rating": 5
        }
    ]
    landing_page.testimonials = json.dumps(testimonials)
    
    # SEO Metadata
    landing_page.meta_title = "Modern IT Solutions | TechStart Solutions"
    landing_page.meta_description = "Transform your business with expert IT consulting services. Cloud migration, cybersecurity, and strategic IT planning."
    
    # Keywords (JSON string)
    keywords = ["IT consulting", "cloud migration", "cybersecurity", "business technology"]
    landing_page.keywords = json.dumps(keywords)
    
    # Open Graph
    landing_page.og_title = "TechStart Solutions - Modern IT Consulting"
    landing_page.og_description = "Expert IT consulting to modernize your business"
    
    # Design
    landing_page.theme = "modern"
    landing_page.primary_color = "#3B82F6"
    landing_page.secondary_color = "#10B981"
    landing_page.html_path = "output/page_1.html"
    landing_page.css_path = "output/style_1.css"
    
    # Status
    landing_page.is_published = True
    landing_page.view_count = 0
    landing_page.created_at = datetime.now()
    landing_page.updated_at = datetime.now()
    
    return landing_page


def test_template_service_initialization():
    """Test that TemplateService initializes correctly."""
    print("\n🧪 Testing TemplateService Initialization...")
    
    service = TemplateService()
    assert service is not None
    assert service.env is not None
    print("✅ TemplateService initialized successfully")


def test_css_generator_initialization():
    """Test that CSSGenerator initializes correctly."""
    print("\n🧪 Testing CSSGenerator Initialization...")
    
    generator = CSSGenerator()
    assert generator is not None
    assert len(generator.THEMES) > 0
    print(f"✅ CSSGenerator initialized with {len(generator.THEMES)} themes")


def test_css_generation():
    """Test CSS generation with different themes."""
    print("\n🧪 Testing CSS Generation...")
    
    generator = get_css_generator()
    
    # Test each theme
    for theme in ['modern', 'minimal', 'bold', 'elegant']:
        css = generator.generate_css(
            theme=theme,
            primary_color='#3B82F6',
            secondary_color='#10B981'
        )
        
        assert css is not None
        assert len(css) > 1000  # CSS should be substantial
        assert 'var(--primary-color)' in css
        assert 'var(--secondary-color)' in css
        assert '.hero-section' in css
        assert '.features-section' in css
        print(f"✅ Generated {len(css)} characters of CSS for '{theme}' theme")


def test_html_rendering():
    """Test HTML rendering with mock data."""
    print("\n🧪 Testing HTML Rendering...")
    
    # Create mock data
    business = create_mock_business()
    landing_page = create_mock_landing_page()
    
    # Render HTML
    service = get_template_service()
    html = service.render_landing_page(
        landing_page=landing_page,
        business=business,
        page_url="https://example.com/page-1",
        powered_by=True
    )
    
    # Verify HTML content
    assert html is not None
    assert len(html) > 500
    assert landing_page.headline in html
    assert landing_page.subheadline in html
    assert 'Cloud Migration' in html  # Feature title
    assert 'Sarah Chen' in html  # Testimonial name
    assert landing_page.meta_title in html
    assert 'TechStart Solutions' in html
    
    print(f"✅ Generated {len(html)} characters of HTML")
    print(f"✅ Verified headline: {landing_page.headline}")
    print(f"✅ Verified features and testimonials in HTML")


def test_file_saving():
    """Test saving HTML and CSS to files."""
    print("\n🧪 Testing File Saving...")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "output" / "test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create mock data
    business = create_mock_business()
    landing_page = create_mock_landing_page()
    
    # Save HTML
    html_path = str(output_dir / "test_page.html")
    service = get_template_service()
    html = service.render_landing_page(landing_page, business)
    saved_html_path = service.save_html_to_file(html, html_path)
    
    assert os.path.exists(saved_html_path)
    print(f"✅ HTML saved to: {saved_html_path}")
    
    # Save CSS
    css_path = str(output_dir / "test_style.css")
    generator = get_css_generator()
    saved_css_path = generator.generate_and_save(
        output_path=css_path,
        theme='modern',
        primary_color='#3B82F6',
        secondary_color='#10B981'
    )
    
    assert os.path.exists(saved_css_path)
    print(f"✅ CSS saved to: {saved_css_path}")
    
    # Verify file sizes
    html_size = os.path.getsize(saved_html_path)
    css_size = os.path.getsize(saved_css_path)
    print(f"✅ HTML file size: {html_size} bytes")
    print(f"✅ CSS file size: {css_size} bytes")


def test_complete_page_generation():
    """Test complete landing page generation (HTML + CSS)."""
    print("\n🧪 Testing Complete Page Generation...")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "output" / "test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create mock data
    business = create_mock_business()
    landing_page = create_mock_landing_page()
    
    # Generate and save HTML
    html_path = str(output_dir / "complete_page.html")
    service = get_template_service()
    saved_html = service.render_and_save(
        landing_page=landing_page,
        output_path=html_path,
        business=business,
        page_url="https://example.com/test",
        powered_by=True
    )
    
    # Generate and save CSS (relative to HTML)
    css_path = str(output_dir / "complete_style.css")
    generator = get_css_generator()
    saved_css = generator.generate_and_save(
        output_path=css_path,
        theme=landing_page.theme,
        primary_color=landing_page.primary_color,
        secondary_color=landing_page.secondary_color
    )
    
    print(f"✅ Complete landing page generated!")
    print(f"   HTML: {saved_html}")
    print(f"   CSS: {saved_css}")
    print(f"\n🌐 Open {saved_html} in a browser to view the page")


def test_responsive_themes():
    """Test all available themes."""
    print("\n🧪 Testing All Themes...")
    
    output_dir = Path(__file__).parent.parent / "output" / "themes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    business = create_mock_business()
    landing_page = create_mock_landing_page()
    
    themes = ['modern', 'minimal', 'bold', 'elegant']
    colors = [
        ('#3B82F6', '#10B981'),  # Blue & Green
        ('#8B5CF6', '#EC4899'),  # Purple & Pink
        ('#F59E0B', '#EF4444'),  # Orange & Red
        ('#06B6D4', '#14B8A6'),  # Cyan & Teal
    ]
    
    for i, (theme, (primary, secondary)) in enumerate(zip(themes, colors)):
        landing_page.theme = theme
        landing_page.primary_color = primary
        landing_page.secondary_color = secondary
        
        # Generate files
        html_path = str(output_dir / f"{theme}_page.html")
        css_path = str(output_dir / f"{theme}_style.css")
        
        service = get_template_service()
        service.render_and_save(landing_page, html_path, business)
        
        generator = get_css_generator()
        generator.generate_and_save(css_path, theme, primary, secondary)
        
        print(f"✅ Generated '{theme}' theme with colors {primary} & {secondary}")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEMPLATE RENDERING INTEGRATION TESTS")
    print("=" * 60)
    
    # Run all tests
    test_template_service_initialization()
    test_css_generator_initialization()
    test_css_generation()
    test_html_rendering()
    test_file_saving()
    test_complete_page_generation()
    test_responsive_themes()
    
    print("\n" + "=" * 60)
    print("✅ ALL TEMPLATE TESTS PASSED!")
    print("=" * 60)
