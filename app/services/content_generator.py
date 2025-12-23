"""
Content Generation Service - Uses AI to generate landing page content.
"""
import json
import re
from typing import Dict, Any, Optional
from app.services.ai_provider import generate_ai_content
from app.services.prompts import PromptTemplates


class ContentGenerationService:
    """Service for generating landing page content using AI."""
    
    def __init__(self):
        """Initialize the content generation service."""
        self.prompt_templates = PromptTemplates()
    
    async def generate_complete_landing_page(
        self,
        business_data: Dict[str, Any],
        num_features: int = 3,
        num_testimonials: int = 2
    ) -> Dict[str, Any]:
        """
        Generate complete landing page content in one call.
        
        Args:
            business_data: Dictionary with business information
            num_features: Number of features to generate
            num_testimonials: Number of testimonials to generate
            
        Returns:
            Dictionary with all landing page content
        """
        # Generate the prompt
        prompt = self.prompt_templates.generate_landing_page_prompt(
            business_data,
            num_features=num_features,
            num_testimonials=num_testimonials
        )
        
        # Generate content using AI
        response = await generate_ai_content(prompt, max_tokens=3000)
        
        # Parse JSON response
        try:
            content = self._extract_json_from_response(response)
            
            # Validate and structure the response
            structured_content = self._structure_landing_page_content(content)
            
            return structured_content
            
        except Exception as e:
            raise Exception(f"Failed to parse AI response: {str(e)}\nResponse: {response[:500]}")
    
    async def generate_headline(self, business_data: Dict[str, Any]) -> str:
        """Generate a headline for the landing page."""
        prompt = self.prompt_templates.generate_headline_prompt(business_data)
        response = await generate_ai_content(prompt, max_tokens=200)
        
        # Extract the best headline from the response
        lines = response.strip().split('\n')
        for line in lines:
            if line.strip() and not line.startswith(('1.', '2.', '3.', 'Best:', 'Why:')):
                # Clean and return first substantial line
                headline = line.strip().strip('"').strip("'").strip('*').strip('-').strip()
                if len(headline) > 10:
                    return headline[:200]  # Limit to 200 chars
        
        # Fallback
        return f"Transform Your {business_data.get('industry', 'Business')}"
    
    async def generate_features(
        self,
        business_data: Dict[str, Any],
        num_features: int = 3
    ) -> list:
        """Generate feature list."""
        prompt = self.prompt_templates.generate_features_prompt(business_data, num_features)
        response = await generate_ai_content(prompt, max_tokens=800)
        
        try:
            features = self._extract_json_from_response(response)
            if isinstance(features, list):
                return features
            elif isinstance(features, dict) and 'features' in features:
                return features['features']
            else:
                raise ValueError("Unexpected features format")
        except Exception:
            # Fallback features
            return self._generate_fallback_features(business_data, num_features)
    
    async def generate_testimonials(
        self,
        business_data: Dict[str, Any],
        num_testimonials: int = 2
    ) -> list:
        """Generate testimonials."""
        prompt = self.prompt_templates.generate_testimonials_prompt(business_data, num_testimonials)
        response = await generate_ai_content(prompt, max_tokens=600)
        
        try:
            testimonials = self._extract_json_from_response(response)
            if isinstance(testimonials, list):
                return testimonials
            elif isinstance(testimonials, dict) and 'testimonials' in testimonials:
                return testimonials['testimonials']
            else:
                raise ValueError("Unexpected testimonials format")
        except Exception:
            # Fallback testimonials
            return self._generate_fallback_testimonials(num_testimonials)
    
    async def generate_seo_metadata(
        self,
        business_data: Dict[str, Any],
        headline: str
    ) -> Dict[str, Any]:
        """Generate SEO metadata."""
        prompt = self.prompt_templates.generate_seo_prompt(business_data, headline)
        response = await generate_ai_content(prompt, max_tokens=400)
        
        try:
            seo = self._extract_json_from_response(response)
            return {
                "meta_title": seo.get("meta_title", headline)[:60],
                "meta_description": seo.get("meta_description", "")[:160],
                "keywords": seo.get("keywords", []),
                "og_title": seo.get("og_title", headline)[:60],
                "og_description": seo.get("og_description", "")[:200]
            }
        except Exception:
            # Fallback SEO
            return self._generate_fallback_seo(business_data, headline)
    
    def _extract_json_from_response(self, response: str) -> Any:
        """
        Extract JSON from AI response (handles markdown code blocks).
        
        Args:
            response: Raw AI response
            
        Returns:
            Parsed JSON object
        """
        # Remove markdown code blocks
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*', '', response)
        response = response.strip()
        
        # Try to find JSON object or array
        json_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                # Try to fix common JSON issues
                json_str = json_str.replace('\n', ' ')  # Remove newlines that might break strings
                json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
                json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays
                return json.loads(json_str)
        
        # If no match, try parsing the whole response
        return json.loads(response)
    
    def _structure_landing_page_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure and validate the landing page content.
        
        Args:
            content: Raw content from AI
            
        Returns:
            Structured and validated content
        """
        # Extract SEO if it's nested
        seo = content.get("seo", {})
        
        structured = {
            "headline": content.get("headline", "")[:200],
            "subheadline": content.get("subheadline", "")[:300],
            "cta_text": content.get("cta_text", "Get Started")[:50],
            "features": content.get("features", []),
            "testimonials": content.get("testimonials", []),
            "meta_title": seo.get("meta_title", content.get("headline", ""))[:60],
            "meta_description": seo.get("meta_description", "")[:160],
            "keywords": seo.get("keywords", []),
            "og_title": seo.get("og_title", content.get("headline", ""))[:60],
            "og_description": seo.get("og_description", "")[:200]
        }
        
        return structured
    
    def _generate_fallback_features(self, business_data: Dict[str, Any], num: int) -> list:
        """Generate fallback features if AI fails."""
        industry = business_data.get("industry", "business")
        features = [
            {
                "title": "Easy to Use",
                "description": f"Our {industry} solution is designed for simplicity and efficiency.",
                "icon": "⚡"
            },
            {
                "title": "Reliable & Secure",
                "description": "Enterprise-grade security and 99.9% uptime guarantee.",
                "icon": "🔒"
            },
            {
                "title": "Expert Support",
                "description": "24/7 customer support from our dedicated team.",
                "icon": "💬"
            }
        ]
        return features[:num]
    
    def _generate_fallback_testimonials(self, num: int) -> list:
        """Generate fallback testimonials if AI fails."""
        testimonials = [
            {
                "name": "Sarah Johnson",
                "role": "CEO",
                "company": "Tech Innovations Inc",
                "content": "This solution transformed our business operations and exceeded our expectations.",
                "rating": 5
            },
            {
                "name": "Michael Chen",
                "role": "Marketing Director",
                "company": "Growth Co",
                "content": "Outstanding results! We saw immediate improvements in our key metrics.",
                "rating": 5
            }
        ]
        return testimonials[:num]
    
    def _generate_fallback_seo(self, business_data: Dict[str, Any], headline: str) -> Dict[str, Any]:
        """Generate fallback SEO if AI fails."""
        name = business_data.get("name", "Business")
        industry = business_data.get("industry", "services")
        
        return {
            "meta_title": f"{name} - {headline}"[:60],
            "meta_description": f"Discover {name}, your trusted {industry} solution. Get started today!"[:160],
            "keywords": [industry, name.lower(), "solution", "services"],
            "og_title": headline[:60],
            "og_description": f"{name} provides exceptional {industry} services."[:200]
        }


# Singleton instance
_content_service = None


def get_content_service() -> ContentGenerationService:
    """Get or create the content generation service instance."""
    global _content_service
    if _content_service is None:
        _content_service = ContentGenerationService()
    return _content_service
