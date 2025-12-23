"""
CSS generation service for creating theme-based stylesheets.
Generates responsive, modern CSS with customizable color schemes.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path


class CSSGenerator:
    """Service for generating custom CSS based on theme and colors."""
    
    # Define theme configurations
    THEMES = {
        'modern': {
            'font_family_heading': "'Poppins', sans-serif",
            'font_family_body': "'Inter', sans-serif",
            'border_radius': '12px',
            'shadow_sm': '0 1px 3px rgba(0, 0, 0, 0.12)',
            'shadow_md': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'shadow_lg': '0 10px 25px rgba(0, 0, 0, 0.15)',
            'transition': '0.3s ease',
            'spacing_unit': '1rem',
        },
        'minimal': {
            'font_family_heading': "'Inter', sans-serif",
            'font_family_body': "'Inter', sans-serif",
            'border_radius': '4px',
            'shadow_sm': '0 1px 2px rgba(0, 0, 0, 0.05)',
            'shadow_md': '0 2px 4px rgba(0, 0, 0, 0.08)',
            'shadow_lg': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'transition': '0.2s ease',
            'spacing_unit': '1rem',
        },
        'bold': {
            'font_family_heading': "'Poppins', sans-serif",
            'font_family_body': "'Inter', sans-serif",
            'border_radius': '8px',
            'shadow_sm': '0 2px 4px rgba(0, 0, 0, 0.15)',
            'shadow_md': '0 6px 12px rgba(0, 0, 0, 0.2)',
            'shadow_lg': '0 12px 30px rgba(0, 0, 0, 0.25)',
            'transition': '0.25s ease',
            'spacing_unit': '1.25rem',
        },
        'elegant': {
            'font_family_heading': "'Poppins', sans-serif",
            'font_family_body': "'Inter', sans-serif",
            'border_radius': '16px',
            'shadow_sm': '0 1px 4px rgba(0, 0, 0, 0.08)',
            'shadow_md': '0 5px 10px rgba(0, 0, 0, 0.12)',
            'shadow_lg': '0 15px 35px rgba(0, 0, 0, 0.18)',
            'transition': '0.35s ease',
            'spacing_unit': '1rem',
        }
    }
    
    def __init__(self):
        """Initialize the CSS generator."""
        pass
    
    def generate_css(
        self,
        theme: str = 'modern',
        primary_color: str = '#3B82F6',
        secondary_color: str = '#10B981'
    ) -> str:
        """
        Generate complete CSS stylesheet.
        
        Args:
            theme: Theme name (modern, minimal, bold, elegant)
            primary_color: Primary brand color (hex)
            secondary_color: Secondary brand color (hex)
            
        Returns:
            Complete CSS string
        """
        # Get theme configuration
        theme_config = self.THEMES.get(theme, self.THEMES['modern'])
        
        # Generate CSS sections
        css_parts = [
            self._generate_css_reset(),
            self._generate_css_variables(primary_color, secondary_color, theme_config),
            self._generate_base_styles(theme_config),
            self._generate_container_styles(theme_config),
            self._generate_button_styles(theme_config),
            self._generate_hero_styles(theme_config),
            self._generate_features_styles(theme_config),
            self._generate_testimonials_styles(theme_config),
            self._generate_cta_styles(theme_config),
            self._generate_footer_styles(theme_config),
            self._generate_utility_styles(theme_config),
            self._generate_responsive_styles()
        ]
        
        return '\n\n'.join(css_parts)
    
    def _generate_css_reset(self) -> str:
        """Generate CSS reset styles."""
        return """/* CSS Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

img, svg {
    max-width: 100%;
    height: auto;
    display: block;
}

a {
    text-decoration: none;
    color: inherit;
}

button {
    border: none;
    background: none;
    cursor: pointer;
    font: inherit;
}"""
    
    def _generate_css_variables(
        self,
        primary_color: str,
        secondary_color: str,
        theme_config: Dict[str, str]
    ) -> str:
        """Generate CSS custom properties."""
        return f"""/* CSS Variables */
:root {{
    /* Colors */
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --text-primary: #1F2937;
    --text-secondary: #6B7280;
    --text-light: #9CA3AF;
    --bg-primary: #FFFFFF;
    --bg-secondary: #F9FAFB;
    --bg-tertiary: #F3F4F6;
    --border-color: #E5E7EB;
    
    /* Typography */
    --font-heading: {theme_config['font_family_heading']};
    --font-body: {theme_config['font_family_body']};
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 1.875rem;
    --font-size-4xl: 2.25rem;
    --font-size-5xl: 3rem;
    
    /* Spacing */
    --spacing-unit: {theme_config['spacing_unit']};
    --spacing-xs: calc(var(--spacing-unit) * 0.5);
    --spacing-sm: var(--spacing-unit);
    --spacing-md: calc(var(--spacing-unit) * 1.5);
    --spacing-lg: calc(var(--spacing-unit) * 2);
    --spacing-xl: calc(var(--spacing-unit) * 3);
    --spacing-2xl: calc(var(--spacing-unit) * 4);
    --spacing-3xl: calc(var(--spacing-unit) * 6);
    
    /* Design tokens */
    --border-radius: {theme_config['border_radius']};
    --border-radius-sm: calc({theme_config['border_radius']} / 2);
    --border-radius-lg: calc({theme_config['border_radius']} * 1.5);
    --shadow-sm: {theme_config['shadow_sm']};
    --shadow-md: {theme_config['shadow_md']};
    --shadow-lg: {theme_config['shadow_lg']};
    --transition: {theme_config['transition']};
    
    /* Layout */
    --container-max-width: 1200px;
    --section-padding: var(--spacing-3xl);
}}"""
    
    def _generate_base_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate base element styles."""
        return """/* Base Styles */
body {
    font-family: var(--font-body);
    color: var(--text-primary);
    background-color: var(--bg-primary);
    font-size: var(--font-size-base);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
    font-weight: 700;
    line-height: 1.2;
    color: var(--text-primary);
}

h1 { font-size: var(--font-size-5xl); }
h2 { font-size: var(--font-size-4xl); }
h3 { font-size: var(--font-size-3xl); }
h4 { font-size: var(--font-size-2xl); }
h5 { font-size: var(--font-size-xl); }
h6 { font-size: var(--font-size-lg); }

p {
    margin-bottom: var(--spacing-sm);
    color: var(--text-secondary);
}"""
    
    def _generate_container_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate container styles."""
        return """/* Container */
.container {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

section {
    padding: var(--section-padding) 0;
}"""
    
    def _generate_button_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate button styles."""
        return """/* Buttons */
.btn {
    display: inline-block;
    padding: var(--spacing-sm) var(--spacing-lg);
    font-weight: 600;
    font-size: var(--font-size-base);
    border-radius: var(--border-radius);
    transition: all var(--transition);
    cursor: pointer;
    text-align: center;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
    box-shadow: var(--shadow-md);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    opacity: 0.9;
}

.btn-secondary {
    background-color: white;
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}

.btn-secondary:hover {
    background-color: var(--primary-color);
    color: white;
    transform: translateY(-2px);
}

.btn-large {
    padding: var(--spacing-md) var(--spacing-xl);
    font-size: var(--font-size-lg);
}"""
    
    def _generate_hero_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate hero section styles."""
        return """/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, white 100%);
    padding: var(--spacing-3xl) 0;
}

.hero-section .container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-2xl);
    align-items: center;
}

.hero-headline {
    font-size: var(--font-size-5xl);
    margin-bottom: var(--spacing-md);
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subheadline {
    font-size: var(--font-size-xl);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xl);
    line-height: 1.6;
}

.hero-cta {
    display: flex;
    gap: var(--spacing-md);
}

.hero-visual {
    display: flex;
    justify-content: center;
    align-items: center;
}

.hero-image-placeholder {
    width: 100%;
    max-width: 500px;
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}"""
    
    def _generate_features_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate features section styles."""
        return """/* Features Section */
.features-section {
    background-color: white;
}

.section-header {
    text-align: center;
    margin-bottom: var(--spacing-3xl);
}

.section-title {
    font-size: var(--font-size-4xl);
    margin-bottom: var(--spacing-sm);
}

.section-subtitle {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-xl);
}

.feature-card {
    padding: var(--spacing-xl);
    background-color: var(--bg-secondary);
    border-radius: var(--border-radius-lg);
    transition: all var(--transition);
    border: 1px solid var(--border-color);
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
}

.feature-icon {
    font-size: var(--font-size-4xl);
    margin-bottom: var(--spacing-md);
    display: inline-block;
}

.feature-title {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--spacing-sm);
    color: var(--text-primary);
}

.feature-description {
    font-size: var(--font-size-base);
    color: var(--text-secondary);
    line-height: 1.7;
}"""
    
    def _generate_testimonials_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate testimonials section styles."""
        return """/* Testimonials Section */
.testimonials-section {
    background-color: var(--bg-secondary);
}

.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--spacing-xl);
}

.testimonial-card {
    padding: var(--spacing-xl);
    background-color: white;
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
    transition: all var(--transition);
}

.testimonial-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.testimonial-rating {
    display: flex;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
}

.testimonial-text {
    font-size: var(--font-size-lg);
    color: var(--text-primary);
    line-height: 1.7;
    margin-bottom: var(--spacing-lg);
    font-style: italic;
}

.testimonial-author {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.author-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: white;
    font-size: var(--font-size-xl);
}

.author-name {
    font-weight: 600;
    font-size: var(--font-size-base);
    color: var(--text-primary);
}

.author-title {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}"""
    
    def _generate_cta_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate CTA section styles."""
        return """/* CTA Section */
.cta-section {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    text-align: center;
}

.cta-headline {
    font-size: var(--font-size-4xl);
    color: white;
    margin-bottom: var(--spacing-md);
}

.cta-subtext {
    font-size: var(--font-size-xl);
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: var(--spacing-xl);
}

.cta-buttons {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
}"""
    
    def _generate_footer_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate footer styles."""
        return """/* Footer */
.footer-section {
    background-color: var(--text-primary);
    color: white;
    padding: var(--spacing-3xl) 0 var(--spacing-lg) 0;
}

.footer-content {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: var(--spacing-xl);
    margin-bottom: var(--spacing-xl);
}

.footer-logo {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--spacing-sm);
    color: white;
}

.footer-tagline {
    color: rgba(255, 255, 255, 0.7);
    font-size: var(--font-size-sm);
}

.footer-heading {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-md);
    color: white;
}

.footer-list {
    list-style: none;
}

.footer-list li {
    margin-bottom: var(--spacing-xs);
}

.footer-list a {
    color: rgba(255, 255, 255, 0.7);
    font-size: var(--font-size-sm);
    transition: color var(--transition);
}

.footer-list a:hover {
    color: var(--primary-color);
}

.footer-bottom {
    padding-top: var(--spacing-lg);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

.footer-copyright {
    color: rgba(255, 255, 255, 0.6);
    font-size: var(--font-size-sm);
}

.footer-powered {
    margin-left: var(--spacing-md);
    color: rgba(255, 255, 255, 0.5);
}"""
    
    def _generate_utility_styles(self, theme_config: Dict[str, str]) -> str:
        """Generate utility classes."""
        return """/* Utilities */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.fade-in-visible {
    opacity: 1;
    transform: translateY(0);
}

.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }

.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }"""
    
    def _generate_responsive_styles(self) -> str:
        """Generate responsive media queries."""
        return """/* Responsive Styles */
@media (max-width: 1024px) {
    .hero-section .container {
        grid-template-columns: 1fr;
        text-align: center;
    }
    
    .hero-cta {
        justify-content: center;
    }
    
    .footer-content {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 768px) {
    :root {
        --font-size-5xl: 2rem;
        --font-size-4xl: 1.75rem;
        --font-size-3xl: 1.5rem;
        --section-padding: var(--spacing-2xl);
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
    
    .testimonials-grid {
        grid-template-columns: 1fr;
    }
    
    .footer-content {
        grid-template-columns: 1fr;
        text-align: center;
    }
    
    .cta-buttons {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
    }
}

@media (max-width: 480px) {
    :root {
        --spacing-unit: 0.875rem;
        --font-size-5xl: 1.75rem;
        --font-size-4xl: 1.5rem;
    }
    
    .hero-headline {
        font-size: var(--font-size-4xl);
    }
}"""
    
    def save_css_to_file(
        self,
        css_content: str,
        output_path: str
    ) -> str:
        """
        Save generated CSS to a file.
        
        Args:
            css_content: CSS string
            output_path: Path where to save the file
            
        Returns:
            Absolute path to the saved file
        """
        try:
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Write CSS to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            return os.path.abspath(output_path)
            
        except Exception as e:
            raise IOError(f"Error saving CSS file: {e}")
    
    def generate_and_save(
        self,
        output_path: str,
        theme: str = 'modern',
        primary_color: str = '#3B82F6',
        secondary_color: str = '#10B981'
    ) -> str:
        """
        Generate and save CSS in one operation.
        
        Args:
            output_path: Path where to save the CSS file
            theme: Theme name
            primary_color: Primary brand color (hex)
            secondary_color: Secondary brand color (hex)
            
        Returns:
            Absolute path to the saved file
        """
        # Generate CSS
        css = self.generate_css(
            theme=theme,
            primary_color=primary_color,
            secondary_color=secondary_color
        )
        
        # Save to file
        saved_path = self.save_css_to_file(css, output_path)
        
        return saved_path


# Singleton instance
_css_generator = None

def get_css_generator() -> CSSGenerator:
    """Get or create the CSSGenerator singleton instance."""
    global _css_generator
    if _css_generator is None:
        _css_generator = CSSGenerator()
    return _css_generator


# Convenience function for direct generation
def generate_landing_page_css(
    theme: str = 'modern',
    primary_color: str = '#3B82F6',
    secondary_color: str = '#10B981',
    output_path: Optional[str] = None
) -> str:
    """
    Convenience function to generate (and optionally save) CSS.
    
    Args:
        theme: Theme name
        primary_color: Primary brand color (hex)
        secondary_color: Secondary brand color (hex)
        output_path: If provided, save CSS to this path
        
    Returns:
        Generated CSS string (and saves to file if output_path provided)
    """
    generator = get_css_generator()
    css = generator.generate_css(theme, primary_color, secondary_color)
    
    if output_path:
        generator.save_css_to_file(css, output_path)
    
    return css
