"""
Tests for Flask Inventory Management API.
"""

import pytest

from app import app
from data import inventory_items


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory_items.clear()
    inventory_items.extend([
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
    ])


def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Welcome to the Inventory Management System API"


def test_get_all_items(client):
    response = client.get("/items")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 2
    assert len(data["items"]) == 2


def test_get_single_item(client):
    response = client.get("/items/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["name"] == "Organic Almond Milk"


def test_get_missing_item_returns_404(client):
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"


def test_create_item(client):
    new_item = {
        "name": "Greek Yogurt",
        "brand": "Brookside",
        "price": 180.00,
        "stock": 10,
        "barcode": "9876543210000",
        "ingredients": "Milk, live cultures",
    }

    response = client.post("/items", json=new_item)
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Item created successfully"
    assert data["item"]["id"] == 3
    assert data["item"]["name"] == "Greek Yogurt"


def test_create_item_missing_required_field(client):
    incomplete_item = {
        "name": "Greek Yogurt",
        "price": 180.00,
    }

    response = client.post("/items", json=incomplete_item)

    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()["error"]


def test_create_item_rejects_negative_price(client):
    bad_item = {
        "name": "Bad Product",
        "brand": "Bad Brand",
        "price": -50,
        "stock": 5,
    }

    response = client.post("/items", json=bad_item)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Price cannot be negative"


def test_update_item(client):
    response = client.put("/items/1", json={
        "price": 300,
        "stock": 15,
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item updated successfully"
    assert data["item"]["price"] == 300.00
    assert data["item"]["stock"] == 15


def test_update_missing_item_returns_404(client):
    response = client.put("/items/999", json={
        "price": 300,
    })

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"


def test_delete_item(client):
    response = client.delete("/items/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item deleted successfully"
    assert data["deleted_item"]["id"] == 1
    assert len(inventory_items) == 1


def test_delete_missing_item_returns_404(client):
    response = client.delete("/items/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"


def test_get_product_from_openfoodfacts_success(client, mocker):
    mocker.patch("app.fetch_product_by_barcode", return_value={
        "name": "Mock Product",
        "brand": "Mock Brand",
        "barcode": "12345",
        "ingredients": "Mock ingredients",
    })

    response = client.get("/items/barcode/12345")
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Mock Product"
    assert data["brand"] == "Mock Brand"


def test_get_product_from_openfoodfacts_failure(client, mocker):
    mocker.patch("app.fetch_product_by_barcode", return_value=None)

    response = client.get("/items/barcode/00000")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found or external API request failed"