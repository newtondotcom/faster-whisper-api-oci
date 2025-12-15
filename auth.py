"""
API Key authentication utilities.
"""
import bcrypt
import secrets
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_api_key() -> str:
    """
    Generate a secure random API key.
    Returns a URL-safe base64-encoded string (43 characters).
    """
    return f"fw_{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key using bcrypt.
    Returns the hashed key as a string.
    """
    return bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """
    Verify an API key against a hashed key.
    Returns True if the key matches, False otherwise.
    """
    try:
        return bcrypt.checkpw(api_key.encode('utf-8'), hashed_key.encode('utf-8'))
    except Exception:
        return False


def get_hashed_api_key_from_env() -> str | None:
    """
    Get the hashed API key from environment variables.
    Returns the hashed key or None if not set.
    """
    return os.getenv('API_KEY_HASH')


def verify_api_key_from_env(api_key: str) -> bool:
    """
    Verify an API key against the hashed key stored in environment variables.
    Returns True if valid, False otherwise.
    """
    hashed_key = get_hashed_api_key_from_env()
    if not hashed_key:
        return False
    return verify_api_key(api_key, hashed_key)

