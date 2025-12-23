"""
Template rendering service for generating HTML from landing page data.
Uses Jinja2 templates to create beautiful, responsive HTML pages.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound

from app.models.landing_page import LandingPage
from app.models.business import Business


class TemplateService:
    """Service for rendering HTML templates with Jinja2."""
    
    def __init__(self):
        """Initialize the Jinja2 environment."""
        # Get the templates directory path
        template_dir = Path(__file__).parent.parent / "templates"
        
        # Create Jinja2 environment with autoescaping for security
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self._register_filters()
    
    def _register_filters(self):
        """Register custom Jinja2 filters."""
        
        def format_date(value, format_string='%B %d, %Y'):
            """Format datetime objects."""
            if isinstance(value, datetime):
                return value.strftime(format_string)
            return value
        
        def truncate_words(text: str, max_words: int = 50) -> str:
            """Truncate text to a specific number of words."""
            words = text.split()
            if len(words) <= max_words:
                return text
            return ' '.join(words[:max_words]) + '...'
        
        def generate_slug(text: str) -> str:
            """Generate URL-friendly slug from text."""
            import re
            text = text.lower()
            text = re.sub(r'[^\w\s-]', '', text)
            text = re.sub(r'[-\s]+', '-', text)
            return text.strip('-')
        
        # Register filters
        self.env.filters['format_date'] = format_date
        self.env.filters['truncate_words'] = truncate_words
        self.env.filters['generate_slug'] = generate_slug
    
    def render_landing_page(
        self,
        landing_page: LandingPage,
        business: Optional[Business] = None,
        page_url: str = "",
        powered_by: bool = True
    ) -> str:
        """
        Render a complete landing page HTML.
        
        Args:
            landing_page: LandingPage model instance
            business: Optional Business model instance (for footer data)
            page_url: Full URL of the page (for Open Graph tags)
            powered_by: Whether to show "Powered by" attribution
            
        Returns:
            Rendered HTML string
        """
        try:
            template = self.env.get_template('landing_page.html')
            
            # Prepare template context
            context = self._prepare_landing_page_context(
                landing_page, 
                business, 
                page_url, 
                powered_by
            )
            
            # Render the template
            html = template.render(**context)
            return html
            
        except TemplateNotFound as e:
            raise FileNotFoundError(f"Template not found: {e}")
        except Exception as e:
            raise RuntimeError(f"Error rendering template: {e}")
    
    def _prepare_landing_page_context(
        self,
        landing_page: LandingPage,
        business: Optional[Business],
        page_url: str,
        powered_by: bool
    ) -> Dict[str, Any]:
        """
        Prepare the context dictionary for template rendering.
        
        Args:
            landing_page: LandingPage model instance
            business: Optional Business model instance
            page_url: Full URL of the page
            powered_by: Whether to show attribution
            
        Returns:
            Dictionary with all template variables
        """
        # Get parsed features and testimonials
        features = landing_page.get_features()
        testimonials = landing_page.get_testimonials()
        keywords = landing_page.get_keywords()
        
        # Build keywords string
        keywords_string = ', '.join(keywords) if keywords else ''
        
        context = {
            # Page identification
            'page_id': landing_page.id,
            'page_url': page_url,
            
            # Hero section
            'headline': landing_page.headline,
            'subheadline': landing_page.subheadline,
            
            # CTA
            'cta_text': landing_page.cta_text,
            'cta_subtext': landing_page.subheadline or 'Start your journey today',
            
            # Features
            'features': features,
            
            # Testimonials
            'testimonials': testimonials,
            
            # SEO Meta Tags
            'meta_title': landing_page.meta_title,
            'meta_description': landing_page.meta_description,
            'keywords_string': keywords_string,
            
            # Open Graph
            'og_title': landing_page.og_title,
            'og_description': landing_page.og_description,
            
            # Design
            'theme': landing_page.theme or 'modern',
            'primary_color': landing_page.primary_color or '#3B82F6',
            'secondary_color': landing_page.secondary_color or '#10B981',
            'css_path': landing_page.css_path or 'style.css',
            
            # Business info (for footer)
            'business_name': business.name if business else 'Your Business',
            'unique_value_proposition': business.unique_value_proposition if business else None,
            
            # Misc
            'current_year': datetime.now().year,
            'powered_by': powered_by,
        }
        
        return context
    
    def save_html_to_file(
        self,
        html_content: str,
        output_path: str
    ) -> str:
        """
        Save rendered HTML to a file.
        
        Args:
            html_content: Rendered HTML string
            output_path: Path where to save the file
            
        Returns:
            Absolute path to the saved file
        """
        try:
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Write HTML to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return os.path.abspath(output_path)
            
        except Exception as e:
            raise IOError(f"Error saving HTML file: {e}")
    
    def render_and_save(
        self,
        landing_page: LandingPage,
        output_path: str,
        business: Optional[Business] = None,
        page_url: str = "",
        powered_by: bool = True
    ) -> str:
        """
        Render and save landing page HTML in one operation.
        
        Args:
            landing_page: LandingPage model instance
            output_path: Path where to save the HTML file
            business: Optional Business model instance
            page_url: Full URL of the page
            powered_by: Whether to show attribution
            
        Returns:
            Absolute path to the saved file
        """
        # Render HTML
        html = self.render_landing_page(
            landing_page=landing_page,
            business=business,
            page_url=page_url,
            powered_by=powered_by
        )
        
        # Save to file
        saved_path = self.save_html_to_file(html, output_path)
        
        return saved_path
    
    def render_preview(
        self,
        landing_page: LandingPage,
        business: Optional[Business] = None
    ) -> str:
        """
        Render a preview version (with mock data if needed).
        
        Args:
            landing_page: LandingPage model instance
            business: Optional Business model instance
            
        Returns:
            Rendered HTML string
        """
        return self.render_landing_page(
            landing_page=landing_page,
            business=business,
            page_url="/preview",
            powered_by=True
        )


# Singleton instance
_template_service = None

def get_template_service() -> TemplateService:
    """Get or create the TemplateService singleton instance."""
    global _template_service
    if _template_service is None:
        _template_service = TemplateService()
    return _template_service


# Convenience function for direct rendering
def render_landing_page_html(
    landing_page: LandingPage,
    business: Optional[Business] = None,
    output_path: Optional[str] = None,
    page_url: str = "",
    powered_by: bool = True
) -> str:
    """
    Convenience function to render (and optionally save) a landing page.
    
    Args:
        landing_page: LandingPage model instance
        business: Optional Business model instance
        output_path: If provided, save HTML to this path
        page_url: Full URL of the page
        powered_by: Whether to show attribution
        
    Returns:
        Rendered HTML string (and saves to file if output_path provided)
    """
    service = get_template_service()
    
    if output_path:
        # Render and save
        service.render_and_save(
            landing_page=landing_page,
            output_path=output_path,
            business=business,
            page_url=page_url,
            powered_by=powered_by
        )
    
    # Always return the rendered HTML
    return service.render_landing_page(
        landing_page=landing_page,
        business=business,
        page_url=page_url,
        powered_by=powered_by
    )
