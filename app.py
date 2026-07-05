"""
Flask REST API for Inventory Management System.
"""

from flask import Flask, jsonify, request

from data import inventory_items, get_next_id
from openfood_api import fetch_product_by_barcode


app = Flask(__name__)


def find_item_by_id(item_id):
    """Find one inventory item by ID."""
    return next((item for item in inventory_items if item["id"] == item_id), None)


def validate_item_payload(data, require_all_fields=True):
    """
    Validate item request data.

    For POST, all required fields are needed.
    For PUT, partial updates are allowed.
    """
    required_fields = ["name", "brand", "price", "stock"]

    if require_all_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}"

    if "price" in data:
        try:
            if float(data["price"]) < 0:
                return "Price cannot be negative"
        except (TypeError, ValueError):
            return "Price must be a number"

    if "stock" in data:
        try:
            if int(data["stock"]) < 0:
                return "Stock cannot be negative"
        except (TypeError, ValueError):
            return "Stock must be an integer"

    return None


@app.route("/")
def home():
    """API welcome route."""
    return jsonify({
        "message": "Welcome to the Inventory Management System API",
        "available_routes": [
            "GET /items",
            "GET /items/<id>",
            "POST /items",
            "PUT /items/<id>",
            "DELETE /items/<id>",
            "GET /items/barcode/<barcode>",
        ],
    }), 200


@app.route("/items", methods=["GET"])
def get_items():
    """Return all inventory items."""
    return jsonify({
        "count": len(inventory_items),
        "items": inventory_items,
    }), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Return one inventory item by ID."""
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@app.route("/items", methods=["POST"])
def create_item():
    """Create a new inventory item."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    validation_error = validate_item_payload(data, require_all_fields=True)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    new_item = {
        "id": get_next_id(),
        "name": data["name"],
        "brand": data["brand"],
        "price": float(data["price"]),
        "stock": int(data["stock"]),
        "barcode": data.get("barcode", ""),
        "ingredients": data.get("ingredients", ""),
    }

    inventory_items.append(new_item)

    return jsonify({
        "message": "Item created successfully",
        "item": new_item,
    }), 201


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """Update an existing inventory item."""
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    validation_error = validate_item_payload(data, require_all_fields=False)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    if "name" in data:
        item["name"] = data["name"]

    if "brand" in data:
        item["brand"] = data["brand"]

    if "price" in data:
        item["price"] = float(data["price"])

    if "stock" in data:
        item["stock"] = int(data["stock"])

    if "barcode" in data:
        item["barcode"] = data["barcode"]

    if "ingredients" in data:
        item["ingredients"] = data["ingredients"]

    return jsonify({
        "message": "Item updated successfully",
        "item": item,
    }), 200


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an inventory item."""
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory_items.remove(item)

    return jsonify({
        "message": "Item deleted successfully",
        "deleted_item": item,
    }), 200


@app.route("/items/barcode/<barcode>", methods=["GET"])
def get_product_from_openfoodfacts(barcode):
    """
    Fetch product data from OpenFoodFacts by barcode.
    """
    product = fetch_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found or external API request failed",
        }), 404

    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)