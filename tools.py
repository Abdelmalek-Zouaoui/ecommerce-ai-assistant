"""
tools.py — Python functions that Claude can call
Owner: MALEK

These are the "tools" Claude uses to fetch real store data.
Each tool receives a store_id so it only returns THAT store's data.
"""

from data import get_products, get_orders


def search_products(store_id: str, query: str) -> list[dict]:
    """Find this store's products whose name, description, or category match query."""
    query = query.lower().strip()
    products = get_products(store_id)
    if not query:
        return products
    return [
        p for p in products
        if query in p["name"].lower()
        or query in p.get("description", "").lower()
        or query in p.get("category", "").lower()
    ]


def get_order_status(store_id: str, order_id: str) -> dict | None:
    """Look up a single order for this store by id, or None if not found."""
    for order in get_orders(store_id):
        if order["id"] == str(order_id):
            return order
    return None
