"""
Tests for OpenFoodFacts API integration.
"""

from unittest.mock import Mock, patch

import requests

from openfood_api import fetch_product_by_barcode


@patch("openfood_api.requests.get")
def test_fetch_product_by_barcode_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, palm oil, hazelnuts, cocoa",
        },
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("3017624010701")

    assert result == {
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "ingredients": "Sugar, palm oil, hazelnuts, cocoa",
    }


@patch("openfood_api.requests.get")
def test_fetch_product_by_barcode_product_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 0,
        "status_verbose": "product not found",
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("0000000000000")

    assert result is None


@patch("openfood_api.requests.get")
def test_fetch_product_by_barcode_handles_request_error(mock_get):
    mock_get.side_effect = requests.RequestException

    result = fetch_product_by_barcode("3017624010701")

    assert result is None


@patch("openfood_api.requests.get")
def test_fetch_product_by_barcode_handles_invalid_json(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError

    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("3017624010701")

    assert result is None


def test_fetch_product_by_barcode_rejects_empty_barcode():
    result = fetch_product_by_barcode("")

    assert result is None