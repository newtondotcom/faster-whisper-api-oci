#!/usr/bin/env python3
"""
Generate a secure API key and its hash for use in .env file.
"""
import sys
from auth import generate_api_key, hash_api_key

def main():
    """Generate and display a new API key and its hash."""
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)
    
    print("=" * 60)
    print("NEW API KEY GENERATED")
    print("=" * 60)
    print(f"\nAPI Key (save this - shown only once!):")
    print(f"{api_key}")
    print(f"\nHashed Key (add to .env file as API_KEY_HASH):")
    print(f"API_KEY_HASH={hashed_key}")
    print("\n" + "=" * 60)
    print("\nTo use this key:")
    print("1. Add the API_KEY_HASH line above to your .env file")
    print("2. Use the API key in your requests:")
    print(f'   curl -H "Authorization: Bearer {api_key}" ...')
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

