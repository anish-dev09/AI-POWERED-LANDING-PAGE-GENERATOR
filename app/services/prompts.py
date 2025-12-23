"""
Prompt templates for AI content generation.
"""
from typing import Dict, Any


class PromptTemplates:
    """Collection of prompt templates for landing page generation."""
    
    @staticmethod
    def generate_landing_page_prompt(business_data: Dict[str, Any], num_features: int = 3, num_testimonials: int = 2) -> str:
        """
        Generate a comprehensive prompt for creating landing page content.
        
        Args:
            business_data: Dictionary with business information
            num_features: Number of features to generate
            num_testimonials: Number of testimonials to generate
            
        Returns:
            Complete prompt string
        """
        name = business_data.get("name", "")
        industry = business_data.get("industry", "")
        target_audience = business_data.get("target_audience", "")
        tone = business_data.get("tone", "professional")
        goal = business_data.get("goal", "")
        uvp = business_data.get("unique_value_proposition", "")
        additional_info = business_data.get("additional_info", "")
        
        prompt = f"""You are an expert marketing copywriter. Create compelling landing page content for the following business:

**Business Name:** {name}
**Industry:** {industry}
**Target Audience:** {target_audience}
**Communication Tone:** {tone}
**Primary Goal:** {goal}
**Unique Value Proposition:** {uvp if uvp else 'N/A'}
**Additional Context:** {additional_info if additional_info else 'N/A'}

Generate the following landing page elements in a structured JSON format:

1. **Headline** (5-10 words): A powerful, attention-grabbing headline that immediately communicates the main benefit
2. **Subheadline** (10-20 words): Supporting text that expands on the headline and adds context
3. **CTA Text** (2-4 words): Compelling call-to-action button text
4. **Features** ({num_features} items): Key features or benefits, each with:
   - title (3-6 words)
   - description (15-30 words)
   - icon (emoji or icon name)
5. **Testimonials** ({num_testimonials} items): Realistic customer testimonials, each with:
   - name (realistic person name)
   - role (job title)
   - company (company name)
   - content (20-40 words of praise)
   - rating (4-5 stars)
6. **SEO Metadata:**
   - meta_title (50-60 characters, include keywords)
   - meta_description (150-160 characters, compelling summary)
   - keywords (5-8 relevant keywords as comma-separated list)
   - og_title (50-60 characters, social media optimized)
   - og_description (150-200 characters, engaging social description)

**Important Guidelines:**
- Match the {tone} tone throughout all content
- Focus on benefits, not just features
- Use action-oriented language
- Make testimonials sound authentic and specific
- Ensure SEO content includes relevant keywords for {industry}
- All content should speak directly to: {target_audience}

**Output Format (JSON):**
```json
{{
  "headline": "...",
  "subheadline": "...",
  "cta_text": "...",
  "features": [
    {{
      "title": "...",
      "description": "...",
      "icon": "..."
    }}
  ],
  "testimonials": [
    {{
      "name": "...",
      "role": "...",
      "company": "...",
      "content": "...",
      "rating": 5
    }}
  ],
  "seo": {{
    "meta_title": "...",
    "meta_description": "...",
    "keywords": ["...", "..."],
    "og_title": "...",
    "og_description": "..."
  }}
}}
```

Generate only the JSON output, no additional text."""
        
        return prompt
    
    @staticmethod
    def generate_headline_prompt(business_data: Dict[str, Any]) -> str:
        """Generate prompt specifically for headline creation."""
        name = business_data.get("name", "")
        industry = business_data.get("industry", "")
        target_audience = business_data.get("target_audience", "")
        uvp = business_data.get("unique_value_proposition", "")
        
        return f"""Create a powerful, attention-grabbing headline (5-10 words) for a landing page.

Business: {name}
Industry: {industry}
Target Audience: {target_audience}
Unique Value: {uvp}

The headline should:
- Immediately communicate the main benefit
- Be clear and memorable
- Speak directly to {target_audience}
- Use action-oriented language

Generate 3 headline options and explain which is best and why."""
    
    @staticmethod
    def generate_features_prompt(business_data: Dict[str, Any], num_features: int = 3) -> str:
        """Generate prompt for creating feature list."""
        name = business_data.get("name", "")
        industry = business_data.get("industry", "")
        goal = business_data.get("goal", "")
        
        return f"""Create {num_features} compelling features for a {industry} business landing page.

Business: {name}
Goal: {goal}

For each feature, provide:
1. Title (3-6 words, benefit-focused)
2. Description (15-30 words, specific and valuable)
3. Icon (relevant emoji or icon name)

Focus on benefits over technical features. Output as JSON array."""
    
    @staticmethod
    def generate_testimonials_prompt(business_data: Dict[str, Any], num_testimonials: int = 2) -> str:
        """Generate prompt for creating testimonials."""
        industry = business_data.get("industry", "")
        target_audience = business_data.get("target_audience", "")
        
        return f"""Create {num_testimonials} realistic customer testimonials for a {industry} business.

Target customers: {target_audience}

For each testimonial, provide:
1. Name (realistic person name)
2. Role (appropriate job title)
3. Company (realistic company name)
4. Content (20-40 words, specific praise with measurable results if possible)
5. Rating (4-5 stars)

Make testimonials sound authentic, not generic. Include specific details. Output as JSON array."""
    
    @staticmethod
    def generate_seo_prompt(business_data: Dict[str, Any], headline: str) -> str:
        """Generate prompt for SEO metadata."""
        name = business_data.get("name", "")
        industry = business_data.get("industry", "")
        target_audience = business_data.get("target_audience", "")
        
        return f"""Create SEO-optimized metadata for a landing page.

Business: {name}
Industry: {industry}
Target Audience: {target_audience}
Headline: {headline}

Generate:
1. meta_title (50-60 chars, include primary keyword)
2. meta_description (150-160 chars, compelling summary with CTA)
3. keywords (5-8 relevant keywords as array)
4. og_title (50-60 chars, social media optimized)
5. og_description (150-200 chars, engaging for social sharing)

Output as JSON object with these exact keys."""
    
    @staticmethod
    def improve_content_prompt(original_content: str, feedback: str) -> str:
        """Generate prompt for improving existing content based on feedback."""
        return f"""Improve the following landing page content based on the feedback provided.

**Original Content:**
{original_content}

**Feedback:**
{feedback}

Generate improved version maintaining the same structure but incorporating the feedback. Output as JSON."""
    
    @staticmethod
    def generate_cta_prompt(business_data: Dict[str, Any], goal: str) -> str:
        """Generate prompt for call-to-action text."""
        tone = business_data.get("tone", "professional")
        
        return f"""Create a compelling call-to-action (CTA) button text (2-4 words) for a landing page.

Goal: {goal}
Tone: {tone}

The CTA should:
- Be action-oriented
- Create urgency or excitement
- Match the {tone} tone
- Be specific to the goal

Provide 5 options and recommend the best one."""
