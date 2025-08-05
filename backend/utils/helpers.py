import logging
import re
import time
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse, urljoin
import hashlib

logger = logging.getLogger(__name__)

def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def normalize_url(url: str) -> str:
    """Normalize URL by adding protocol if missing"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(normalize_url(url))
        return parsed.netloc.replace('www.', '')
    except:
        return url

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32)
    
    return text.strip()

def truncate_text(text: str, max_length: int = 160) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    # Try to break at word boundary
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.8:  # If space is reasonably close to end
        truncated = truncated[:last_space]
    
    return truncated + "..."

def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes"""
    if not text:
        return 0
    
    word_count = len(text.split())
    reading_time = max(1, round(word_count / words_per_minute))
    return reading_time

def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text"""
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return re.findall(phone_pattern, text)

def generate_cache_key(url: str, params: Optional[Dict] = None) -> str:
    """Generate cache key for URL and parameters"""
    key_parts = [url]
    
    if params:
        sorted_params = sorted(params.items())
        param_string = "&".join(f"{k}={v}" for k, v in sorted_params)
        key_parts.append(param_string)
    
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def format_number(number: Union[int, float], format_type: str = "compact") -> str:
    """Format numbers for display"""
    if format_type == "compact":
        if number >= 1_000_000:
            return f"{number/1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number/1_000:.1f}K"
        else:
            return str(int(number))
    elif format_type == "comma":
        return f"{number:,}"
    else:
        return str(number)

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    
    return ((new_value - old_value) / old_value) * 100

def is_valid_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_keywords_from_text(text: str, min_length: int = 3, max_keywords: int = 50) -> List[str]:
    """Extract potential keywords from text using simple heuristics"""
    if not text:
        return []
    
    # Clean text and convert to lowercase
    clean = re.sub(r'[^\w\s]', ' ', text.lower())
    words = clean.split()
    
    # Filter words by length and remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'this', 'that',
        'these', 'those', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
        'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he',
        'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
        'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
        'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
        'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'having', 'do', 'does', 'did', 'doing', 'will', 'would', 'should',
        'could', 'can', 'may', 'might', 'must', 'shall'
    }
    
    filtered_words = [
        word for word in words 
        if len(word) >= min_length and word not in stop_words and word.isalpha()
    ]
    
    # Count word frequencies
    from collections import Counter
    word_counts = Counter(filtered_words)
    
    # Return most common words
    return [word for word, count in word_counts.most_common(max_keywords)]

def get_url_depth(url: str) -> int:
    """Calculate URL depth (number of path segments)"""
    try:
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        return len(path.split('/')) if path else 0
    except:
        return 0

def is_internal_link(url: str, base_domain: str) -> bool:
    """Check if URL is internal to the base domain"""
    try:
        parsed_url = urlparse(url)
        parsed_base = urlparse(base_domain)
        
        url_domain = parsed_url.netloc.replace('www.', '')
        base_domain_clean = parsed_base.netloc.replace('www.', '')
        
        return url_domain == base_domain_clean
    except:
        return False

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def safe_divide(numerator: Union[int, float], denominator: Union[int, float], default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

def get_domain_extension(domain: str) -> str:
    """Extract domain extension from domain name"""
    try:
        parts = domain.split('.')
        return parts[-1] if len(parts) > 1 else ""
    except:
        return ""

def is_commercial_keyword(keyword: str) -> bool:
    """Check if keyword has commercial intent"""
    commercial_indicators = [
        'buy', 'purchase', 'order', 'shop', 'store', 'sale', 'deal', 'discount',
        'price', 'cost', 'cheap', 'affordable', 'best', 'top', 'review',
        'compare', 'vs', 'versus', 'alternative', 'software', 'tool', 'service'
    ]
    
    keyword_lower = keyword.lower()
    return any(indicator in keyword_lower for indicator in commercial_indicators)

def get_content_type_from_url(url: str) -> str:
    """Guess content type based on URL structure"""
    url_lower = url.lower()
    
    if '/blog/' in url_lower or '/article/' in url_lower:
        return 'blog'
    elif '/product/' in url_lower or '/shop/' in url_lower:
        return 'product'
    elif '/service/' in url_lower:
        return 'service'
    elif '/about' in url_lower:
        return 'about'
    elif '/contact' in url_lower:
        return 'contact'
    elif '/pricing' in url_lower or '/price' in url_lower:
        return 'pricing'
    elif '/guide/' in url_lower or '/tutorial/' in url_lower:
        return 'guide'
    else:
        return 'page'

class RateLimiter:
    """Simple rate limiter for API requests"""
    
    def __init__(self, max_requests: int = 60, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for given identifier"""
        current_time = time.time()
        
        # Clean old entries
        self.requests = {
            k: v for k, v in self.requests.items() 
            if current_time - v['first_request'] < self.time_window
        }
        
        # Check current identifier
        if identifier not in self.requests:
            self.requests[identifier] = {
                'count': 1,
                'first_request': current_time
            }
            return True
        
        # Check if within limits
        if self.requests[identifier]['count'] < self.max_requests:
            self.requests[identifier]['count'] += 1
            return True
        
        return False
    
    def get_reset_time(self, identifier: str) -> Optional[float]:
        """Get when the rate limit resets for an identifier"""
        if identifier in self.requests:
            return self.requests[identifier]['first_request'] + self.time_window
        return None

# Global rate limiter instance
rate_limiter = RateLimiter()

def log_performance(func_name: str, start_time: float, end_time: float, **kwargs):
    """Log performance metrics for functions"""
    duration = end_time - start_time
    logger.info(f"Performance: {func_name} took {duration:.3f}s", extra=kwargs)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    max_length = 255
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        name = name[:max_length - len(ext) - 1]
        filename = f"{name}.{ext}" if ext else name
    
    return filename.strip()
