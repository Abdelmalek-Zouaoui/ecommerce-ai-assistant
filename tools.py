"""
tools.py — Python functions that Claude can call
Owner: MALEK

These are the "tools" Claude uses to fetch real store data.
Each tool receives a store_id so it only returns THAT store's data.
"""

import difflib

from data import get_products, get_orders

FUZZY_CUTOFF = 0.7
REQUIRED_PRODUCT_FIELDS = {"id", "name", "price", "stock"}
REQUIRED_ORDER_FIELDS = {"id", "status"}


def _well_formed(records: list, required_fields: set) -> bool:
    return all(
        isinstance(r, dict) and required_fields.issubset(r.keys())
        for r in records
    )


def _matches(query_words: list[str], product: dict) -> bool:
    haystack = f"{product['name']} {product.get('description', '')} {product.get('category', '')}".lower()
    if all(qw in haystack for qw in query_words):
        return True
    haystack_words = haystack.split()
    return any(
        any(qw in hw or hw in qw for hw in haystack_words)
        or difflib.get_close_matches(qw, haystack_words, n=1, cutoff=FUZZY_CUTOFF)
        for qw in query_words
    )


def search_products(store_id: str, query: str) -> list[dict] | dict:
    """Find this store's products whose name, description, or category match query
    (tolerates minor spelling/plural variants, e.g. 'hoody' matches 'Hoodie')."""
    try:
        products = get_products(store_id)
    except FileNotFoundError:
        return {"error": "store data unavailable"}
    if not _well_formed(products, REQUIRED_PRODUCT_FIELDS):
        return {"error": "store data malformed"}
    query = query.lower().strip()
    if not query:
        return products
    query_words = query.split()
    return [p for p in products if _matches(query_words, p)]


def get_order_status(store_id: str, order_id: str) -> dict | None:
    """Look up a single order for this store by id, or None if not found."""
    try:
        orders = get_orders(store_id)
    except FileNotFoundError:
        return {"error": "store data unavailable"}
    if not _well_formed(orders, REQUIRED_ORDER_FIELDS):
        return {"error": "store data malformed"}
    for order in orders:
        if order["id"] == str(order_id):
            return order
    return None
