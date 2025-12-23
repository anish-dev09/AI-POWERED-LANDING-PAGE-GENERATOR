"""
Utility functions for content processing and validation.
"""
import re
import json
from typing import Any, Dict, List, Optional
from datetime import datetime


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text by removing extra whitespace and limiting length.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length (optional)
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text


def validate_hex_color(color: str) -> bool:
    """
    Validate if a string is a valid hex color.
    
    Args:
        color: Color string to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^#[0-9A-Fa-f]{6}$'
    return bool(re.match(pattern, color))


def format_keywords(keywords: List[str]) -> List[str]:
    """
    Format and clean keyword list.
    
    Args:
        keywords: List of keywords
        
    Returns:
        Cleaned and formatted keyword list
    """
    if not keywords:
        return []
    
    # Clean and lowercase
    cleaned = []
    for keyword in keywords:
        keyword = keyword.strip().lower()
        if keyword and keyword not in cleaned:
            cleaned.append(keyword)
    
    return cleaned[:10]  # Limit to 10 keywords


def generate_slug(text: str) -> str:
    """
    Generate URL-friendly slug from text.
    
    Args:
        text: Text to convert to slug
        
    Returns:
        URL-friendly slug
    """
    # Convert to lowercase
    slug = text.lower()
    
    # Replace spaces and special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug[:100]  # Limit length


def calculate_reading_time(text: str) -> int:
    """
    Calculate estimated reading time in minutes.
    
    Args:
        text: Text content
        
    Returns:
        Reading time in minutes
    """
    words = len(text.split())
    # Average reading speed: 200 words per minute
    minutes = max(1, round(words / 200))
    return minutes


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length at word boundary.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Truncate at word boundary
    truncated = text[:max_length - len(suffix)].rsplit(' ', 1)[0]
    return truncated + suffix


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: URL string
        
    Returns:
        Domain name
    """
    pattern = r'(?:https?://)?(?:www\.)?([^/]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else url


def validate_json_string(json_string: str) -> bool:
    """
    Validate if a string is valid JSON.
    
    Args:
        json_string: String to validate
        
    Returns:
        True if valid JSON, False otherwise
    """
    try:
        json.loads(json_string)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def parse_json_safely(json_string: str, default: Any = None) -> Any:
    """
    Safely parse JSON string with fallback.
    
    Args:
        json_string: JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    if not json_string:
        return default
    
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merge two dictionaries, with dict2 values taking precedence.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def clean_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Text with HTML tags
        
    Returns:
        Text without HTML tags
    """
    return re.sub(r'<[^>]+>', '', text)


def capitalize_first_letter(text: str) -> str:
    """
    Capitalize first letter of text.
    
    Args:
        text: Text to capitalize
        
    Returns:
        Text with first letter capitalized
    """
    return text[0].upper() + text[1:] if text else text


def format_phone_number(phone: str) -> str:
    """
    Format phone number to standard format.
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone number
    """
    # Remove non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format


def generate_unique_filename(base_name: str, extension: str) -> str:
    """
    Generate unique filename with timestamp.
    
    Args:
        base_name: Base name for the file
        extension: File extension
        
    Returns:
        Unique filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = generate_slug(base_name)
    return f"{slug}_{timestamp}.{extension.lstrip('.')}"


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


def extract_numbers(text: str) -> List[int]:
    """
    Extract all numbers from text.
    
    Args:
        text: Text to extract numbers from
        
    Returns:
        List of integers found in text
    """
    return [int(num) for num in re.findall(r'\d+', text)]


def is_valid_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
