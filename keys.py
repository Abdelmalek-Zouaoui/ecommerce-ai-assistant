"""
keys.py — API key → store_id mapping
Owner: AMINE

Each store gets a hand-made key. This module checks if a key is valid
and returns which store it belongs to.
"""

# A3: Hand-made keys — each store gets one
KEYS = {
    "sk_store_a": "store_a",
    "sk_store_b": "store_b",
}


def get_store_id(api_key):
    """
    Look up an API key and return the store_id.
    Returns None if the key is invalid.
    """
    return KEYS.get(api_key)
