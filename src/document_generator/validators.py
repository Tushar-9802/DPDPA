"""
Input validation and sanitization for document generation.
Ensures safe handling of user-provided data.
"""

import re
from typing import Dict, Any, List

class ValidationError(Exception):
    """Raised when profile validation fails"""
    pass

def validate_profile(profile: dict) -> dict:
    """
    Validate business profile has minimum required fields.
    
    Args:
        profile: Business profile dictionary from assessment
        
    Returns:
        Validated profile with type conversions
        
    Raises:
        ValidationError: If required fields missing or invalid
    """
    # Check required fields
    required_fields = ['business_name', 'entity_type', 'data_types']
    
    for field in required_fields:
        if field not in profile or not profile[field]:
            raise ValidationError(f"Required field missing: {field}")
    
    # Validate business_name is non-empty string
    if not isinstance(profile['business_name'], str) or not profile['business_name'].strip():
        raise ValidationError("business_name must be a non-empty string")
    
    # Validate entity_type
    from .constants import VALID_ENTITY_TYPES
    if profile['entity_type'] not in VALID_ENTITY_TYPES:
        raise ValidationError(
            f"Invalid entity_type: {profile['entity_type']}. "
            f"Must be one of: {', '.join(VALID_ENTITY_TYPES)}"
        )
    
    # Validate data_types is non-empty list
    if not isinstance(profile['data_types'], list):
        raise ValidationError("data_types must be a list")
    
    if not profile['data_types']:
        raise ValidationError("data_types cannot be empty")
    
    # Validate user_count if present
    if 'user_count' in profile:
        try:
            profile['user_count'] = int(profile['user_count'])
            if profile['user_count'] < 0:
                raise ValidationError("user_count cannot be negative")
        except (TypeError, ValueError):
            raise ValidationError("user_count must be a valid integer")
    
    # Validate boolean flags
    boolean_fields = [
        'processes_children_data',
        'has_processors',
        'has_consent_mechanism',
        'has_breach_plan',
        'has_grievance_system'
    ]
    
    for field in boolean_fields:
        if field in profile and not isinstance(profile[field], bool):
            # Try to convert to boolean
            if profile[field] in ['true', 'True', '1', 1]:
                profile[field] = True
            elif profile[field] in ['false', 'False', '0', 0]:
                profile[field] = False
            else:
                raise ValidationError(f"{field} must be a boolean")
    
    return profile

def sanitize_input(text: str) -> str:
    """
    Remove potentially dangerous characters from user input.
    
    Args:
        text: Raw user input string
        
    Returns:
        Sanitized string safe for document insertion
    """
    if not text:
        return ''
    
    # Convert to string if not already
    text = str(text)
    
    # Remove control characters (except newline, return, tab)
    sanitized = ''.join(
        char for char in text 
        if ord(char) >= 32 or char in '\n\r\t'
    )
    
    # Remove potentially malicious patterns
    sanitized = re.sub(r'[<>{}]', '', sanitized)
    
    # Remove excessive whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    return sanitized.strip()

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address string
        
    Returns:
        True if valid email format, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate Indian phone number format.
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid Indian phone format, False otherwise
    """
    if not phone:
        return False
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check for valid Indian phone patterns
    patterns = [
        r'^\+91[6-9]\d{9}$',  # +91 prefix
        r'^91[6-9]\d{9}$',    # 91 prefix without +
        r'^[6-9]\d{9}$'       # 10-digit mobile
    ]
    
    return any(re.match(pattern, cleaned) for pattern in patterns)

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file creation.
    
    Args:
        filename: Proposed filename
        
    Returns:
        Safe filename with dangerous characters removed
    """
    # Remove path separators and dangerous characters
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', filename)
    
    # Limit length
    if len(sanitized) > 100:
        name_part = sanitized[:90]
        ext_part = sanitized[-10:] if '.' in sanitized[-10:] else ''
        sanitized = name_part + ext_part
    
    return sanitized