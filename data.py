"""
data.py — Load product/order data for a given store
Owner: AMINE

Reads from data/<store_id>/products.json and data/<store_id>/orders.json.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def _load(store_id: str, filename: str) -> list[dict]:
    path = DATA_DIR / store_id / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_products(store_id: str) -> list[dict]:
    return _load(store_id, "products.json")


def get_orders(store_id: str) -> list[dict]:
    return _load(store_id, "orders.json")
