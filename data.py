"""
data.py — Load product/order data for a given store
Owner: AMINE

Reads from data/<store_id>/products.json and data/<store_id>/orders.json.
"""

import json
import os


def get_products(store_id):
    """
    Load all products for a store from its JSON file.

    Args:
        store_id: which store to load (e.g. "store_a")

    Returns:
        A list of product dicts, or an empty list if the store doesn't exist.
    """
    path = os.path.join("data", store_id, "products.json")
    if not os.path.exists(path):
        return []  # no products found for this store
    with open(path, "r") as f:
        return json.load(f)


def get_orders(store_id):
    """
    Load all orders for a store from its JSON file.

    Args:
        store_id: which store to load (e.g. "store_a")

    Returns:
        A list of order dicts, or an empty list if the store doesn't exist.
    """
    path = os.path.join("data", store_id, "orders.json")
    if not os.path.exists(path):
        return []  # no orders found for this store
    with open(path, "r") as f:
        return json.load(f)
