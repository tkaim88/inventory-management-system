"""
Command-line client for testing the Inventory Management System API.
"""

import requests


BASE_URL = "http://127.0.0.1:5000"


def display_menu():
    print("\nInventory Management System CLI")
    print("1. View all items")
    print("2. View item by ID")
    print("3. Add item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Fetch product by barcode from OpenFoodFacts")
    print("7. Exit")


def view_all_items():
    response = requests.get(f"{BASE_URL}/items")
    print(response.json())


def view_item_by_id():
    item_id = input("Enter item ID: ")
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    print(response.json())


def add_item():
    item = {
        "name": input("Name: "),
        "brand": input("Brand: "),
        "price": float(input("Price: ")),
        "stock": int(input("Stock: ")),
        "barcode": input("Barcode: "),
        "ingredients": input("Ingredients: "),
    }

    response = requests.post(f"{BASE_URL}/items", json=item)
    print(response.json())


def update_item():
    item_id = input("Enter item ID to update: ")

    print("Leave a field blank if you do not want to update it.")
    updated_data = {}

    name = input("New name: ")
    brand = input("New brand: ")
    price = input("New price: ")
    stock = input("New stock: ")
    barcode = input("New barcode: ")
    ingredients = input("New ingredients: ")

    if name:
        updated_data["name"] = name
    if brand:
        updated_data["brand"] = brand
    if price:
        updated_data["price"] = float(price)
    if stock:
        updated_data["stock"] = int(stock)
    if barcode:
        updated_data["barcode"] = barcode
    if ingredients:
        updated_data["ingredients"] = ingredients

    response = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_data)
    print(response.json())


def delete_item():
    item_id = input("Enter item ID to delete: ")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    print(response.json())


def fetch_product_by_barcode():
    barcode = input("Enter product barcode: ")
    response = requests.get(f"{BASE_URL}/items/barcode/{barcode}")
    print(response.json())


def main():
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_item_by_id()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            fetch_product_by_barcode()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()