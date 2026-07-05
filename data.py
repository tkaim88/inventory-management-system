"""
Temporary in-memory inventory database

This file simulates data storage using a Python list.
Each inventory item must have a unique ID.
"""

inventory_items = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 250.00,
        "stock": 12,
        "barcode": "0037000802261",
        "ingredients": "Filtered water, almonds, cane sugar",
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "brand": "Generic Bakery",
        "price": 120.00,
        "stock": 20,
        "barcode": "1234567890123",
        "ingredients": "Whole wheat flour, water, yeast, salt",
    },
]


def get_next_id():
    """Return the next available item ID."""
    if not inventory_items:
        return 1

    return max(item["id"] for item in inventory_items) + 1