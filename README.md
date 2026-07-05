# Inventory Management System API

## Student

**Name:** Thomas Buko  
**Course:** Moringa School – Module 5  
**Project:** Summative Lab – Python REST API with Flask Inventory Management System

---

## Project Description

This is a Flask-based REST API for managing inventory items. The system supports full CRUD operations and integrates with the OpenFoodFacts API to fetch product information using a barcode.

The project uses an in-memory Python list as temporary storage.

---

## Features

- View all inventory items
- View a single inventory item by ID
- Add a new inventory item
- Update an existing inventory item
- Delete an inventory item
- Fetch product details from OpenFoodFacts by barcode
- Test API routes using pytest
- Mock external API requests using unittest.mock

---

## Technologies Used

- Python 3
- Flask
- Requests
- Pytest
- Pytest Mock
- OpenFoodFacts API

---

## Project Structure

```text
inventory-management-system/
├── app.py
├── cli.py
├── data.py
├── openfood_api.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    ├── __init__.py
    ├── test_app.py
    └── test_openfood_api.py