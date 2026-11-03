
import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = "inventory.json"


def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as file:
            return json.load(file)
    return []


def create_oop_inventory():
    old_inventory = load_inventory()
    inventory = Inventory()

    for item in old_inventory:
        product = Product(
            item["id"],
            item["name"],
            item["price"],
            item["stock"]
        )
        inventory.add_product(product)

    return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully.")


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip().upper()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if not 0 <= price < float("inf") or stock < 0:
            print("Price and stock must be non-negative.")
            return

    except ValueError:
        print("Invalid price or stock quantity.")
        return

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    product.display_information()

    try:
        quantity = int(input("New Stock Quantity: "))
        product.update_stock(quantity)
    except ValueError:
        print("Invalid stock quantity.")


def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is not None:
        product.display_information()
    else:
        print("Product not found.")


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("INVENTORY MANAGEMENT SYSTEM")

    inventory = create_oop_inventory()

    while True:
        show_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            save_inventory(inventory)

        elif option == "6":
            save_inventory(inventory)
            print("Program terminated.")
            break

        else:
            print("Invalid option. Choose 1 to 6.")


if __name__ == "__main__":
    main()
