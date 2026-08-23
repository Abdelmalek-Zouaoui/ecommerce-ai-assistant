"""
keys.py — API key → store_id mapping
Owner: AMINE

Each store gets a hand-made key. This module checks if a key is valid
and returns which store it belongs to.
"""

VALID_KEYS = {
    "sk_store_a": "store_a",
    "sk_store_b": "store_b",
}

def get_store_id(api_key: str) -> str:
    """Return the store_id for a given api_key, or None if invalid."""
    return VALID_KEYS.get(api_key)
