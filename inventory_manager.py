import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

INVENTORY_FILE = "inventory.json"


def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def create_oop_inventory():
    old_inventory = load_inventory()
    inventory = Inventory()

    for item in old_inventory:
        product_type = item.get("type", "physical")

        if product_type == "physical":
            product = PhysicalProduct(
                item["id"],
                item["name"],
                item["price"],
                item["stock"],
                item.get("weight", 0)
            )

        elif product_type == "digital":
            product = DigitalProduct(
                item["id"],
                item["name"],
                item["price"],
                item["stock"],
                item["download_size"]
            )

        else:
            raise ValueError("Unknown product type.")

        if not inventory.add_product(product):
            raise ValueError("Duplicate product ID in inventory.json.")

    return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully.")


def add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip().upper()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if not 0 <= price < float("inf") or stock < 0:
            print("Price and stock must be non-negative.")
            return

        if product_type == "1":
            weight = float(input("Weight (kg): "))

            if not 0 <= weight < float("inf"):
                print("Invalid weight.")
                return

            product = PhysicalProduct(
                product_id, name, price, stock, weight
            )

        else:
            download_size = float(input("Download Size (MB): "))

            if not 0 <= download_size < float("inf"):
                print("Invalid download size.")
                return

            product = DigitalProduct(
                product_id, name, price, stock, download_size
            )

        inventory.add_product(product)

    except ValueError:
        print("Invalid input. Please enter valid numbers.")


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
    print("INVENTORY MANAGEMENT SYSTEM - LAB 7")

    try:
        inventory = create_oop_inventory()
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Unable to load inventory: {error}")
        return

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
