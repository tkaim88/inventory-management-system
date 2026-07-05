# Inventory Management System API

## Student

**Name:** Thomas Komora Buko  
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

## API Routes
Method	Route	Description
GET	/	API welcome route
GET	/items	Get all inventory items
GET	/items/<id>	Get one inventory item
POST	/items	Create a new inventory item
PUT	/items/<id>	Update an inventory item
DELETE	/items/<id>	Delete an inventory item
GET	/items/barcode/<barcode>	Fetch product details from OpenFoodFacts
Example Item JSON
{
  "name": "Greek Yogurt",
  "brand": "Brookside",
  "price": 180.00,
  "stock": 10,
  "barcode": "9876543210000",
  "ingredients": "Milk, live cultures"
}
## Running the Project

Activate your virtual environment:

source venv/bin/activate

Install dependencies if needed:

pip install -r requirements.txt

Run the Flask API:

python app.py

The API will run at:

http://127.0.0.1:5000
Running the CLI

## Open another terminal, activate the environment, then run:

source venv/bin/activate
python cli.py
Running Tests

## Install test dependencies:

pip install pytest pytest-mock
pip freeze > requirements.txt

## Run tests:

pytest

Run tests with detailed output:

pytest -v.

## This project demonstrates Flask routing, CRUD operations, external API integration, testing, and Git workflow management.