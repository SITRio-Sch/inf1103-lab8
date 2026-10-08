import json
import os


INVENTORY_FILE = "inventory.json"


def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        print("Inventory loaded successfully.")
        return inventory

    print("inventory.json not found. Starting with an empty inventory.")
    return []


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)


def display_all(inventory):
    print("\nCurrent Inventory")
    if not inventory:
        print("No products in inventory.")
        return

    print("------------------------------------------------")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("------------------------------------------------")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    # Check the ID before asking for the other details.
    for product in inventory:
        if product["id"].strip().upper() == product_id:
            print("Product ID already exists.")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
    except ValueError:
        print("Invalid price. Enter a non-negative number.")
        return

    if not 0 <= price < float("inf"):
        print("Invalid price. Enter a non-negative number.")
        return

    try:
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid stock quantity. Enter a non-negative integer.")
        return

    if stock < 0:
        print("Invalid stock quantity. Enter a non-negative integer.")
        return

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    })
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:
        if product["id"].strip().upper() == product_id:
            print("\nProduct Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")
            print()

            try:
                stock = int(input("New Stock Quantity: "))
            except ValueError:
                print("Invalid stock quantity. Enter a non-negative integer.")
                return

            if stock < 0:
                print("Invalid stock quantity. Enter a non-negative integer.")
                return

            product["stock"] = stock
            print("Stock updated successfully!")
            return

    print("Product not found.")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:
        if product["id"].strip().upper() == product_id:
            print("\nProduct Found")
            print("------------------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("------------------------------------------------")
            return

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
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    print()
    inventory = load_inventory()
    show_menu()

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print()
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            show_menu()


if __name__ == "__main__":
    main()
