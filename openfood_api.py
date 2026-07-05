"""
OpenFoodFacts API integration.

This module fetches product information from OpenFoodFacts using a barcode.
"""

import requests


OPENFOODFACTS_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"


def fetch_product_by_barcode(barcode):
    """
    Fetch product information from OpenFoodFacts using a barcode.

    Returns:
        dict: Product details if found.
        None: If product is not found or request fails.
    """
    if not barcode:
        return None

    try:
        response = requests.get(
            OPENFOODFACTS_URL.format(barcode=barcode),
            timeout=10,
            headers={
                "User-Agent": "InventoryManagementSystem/1.0 (Student Project)"
            },
        )
        response.raise_for_status()

        data = response.json()

        product = data.get("product")
        if not product:
            return None

        return {
            "name": product.get("product_name") or "Unknown Product",
            "brand": product.get("brands") or "Unknown Brand",
            "barcode": barcode,
            "ingredients": product.get("ingredients_text") or "Ingredients not available",
        }

    except requests.RequestException:
        return None
    except ValueError:
        return None