import re
from typing import List


def sanitize_string(value: str, max_length: int = 500) -> str:
    if not isinstance(value, str):
        return str(value)
    value = value.strip()
    if len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    pattern = r'^[a-zA-Z0-9_-]{3,100}$'
    return bool(re.match(pattern, username))


def validate_password_strength(password: str) -> tuple[bool, List[str]]:
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")
    
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors
