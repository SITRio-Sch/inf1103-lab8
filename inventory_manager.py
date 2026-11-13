import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import ProductData
from supplier import Supplier

INVENTORY_FILE = "inventory.json"

# Shared by every old record that has no supplier of its own.
DEFAULT_SUPPLIER = Supplier("S000", "Unknown Supplier", "unknown@example.com")


def load_inventory() -> list[ProductData]:
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def get_supplier_for_record(
    item: ProductData,
    supplier_cache: dict[str, Supplier]
) -> Supplier:
    supplier_data = item.get("supplier")

    if not isinstance(supplier_data, dict):
        return DEFAULT_SUPPLIER

    # The same supplier ID always gives back the same Supplier object.
    supplier_id = str(supplier_data["id"])

    if supplier_id not in supplier_cache:
        supplier_cache[supplier_id] = Supplier(
            supplier_id,
            str(supplier_data["name"]),
            str(supplier_data["contact_email"])
        )

    return supplier_cache[supplier_id]


def create_oop_inventory() -> Inventory:
    old_inventory = load_inventory()
    inventory = Inventory()
    supplier_cache: dict[str, Supplier] = {}

    for item in old_inventory:
        product_type = item.get("type", "physical")
        supplier = get_supplier_for_record(item, supplier_cache)

        if product_type == "physical":
            product = PhysicalProduct(
                str(item["id"]),
                str(item["name"]),
                float(item["price"]),
                int(item["stock"]),
                float(item.get("weight", 0)),
                supplier
            )

        elif product_type == "digital":
            product = DigitalProduct(
                str(item["id"]),
                str(item["name"]),
                float(item["price"]),
                int(item["stock"]),
                float(item["download_size"]),
                supplier
            )

        else:
            raise ValueError("Unknown product type.")

        if not inventory.add_product(product):
            raise ValueError("Duplicate product ID in inventory.json.")

    return inventory


def save_inventory(inventory: Inventory) -> None:
    data: list[ProductData] = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully.")


def find_existing_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    for product in inventory.get_products():
        if product.supplier.supplier_id == supplier_id:
            return product.supplier

    return None


def ask_for_supplier(inventory: Inventory) -> Supplier | None:
    supplier_id = input("Supplier ID: ").strip().upper()

    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None

    existing_supplier = find_existing_supplier(inventory, supplier_id)

    if existing_supplier is not None:
        print(f"Using existing supplier: {existing_supplier.name}")
        return existing_supplier

    name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Email: ").strip()

    if not name or not contact_email:
        print("Supplier name and email cannot be empty.")
        return None

    return Supplier(supplier_id, name, contact_email)


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip().upper()

    if inventory.find_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return

    supplier = ask_for_supplier(inventory)

    if supplier is None:
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
                product_id, name, price, stock, weight, supplier
            )

        else:
            download_size = float(input("Download Size (MB): "))

            if not 0 <= download_size < float("inf"):
                print("Invalid download size.")
                return

            product = DigitalProduct(
                product_id, name, price, stock, download_size, supplier
            )

        inventory.add_product(product)

    except ValueError:
        print("Invalid input. Please enter valid numbers.")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    product.display_information()

    try:
        quantity = int(input("New Stock Quantity: "))
        product.update_stock(quantity)
    except ValueError:
        print("Invalid stock quantity.")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is not None:
        product.display_information()
    else:
        print("Product not found.")


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")

    product_id = input("Enter Product ID: ").strip().upper()
    inventory.remove_product(product_id)


def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Save Inventory")
    print("7. Exit")
    print("----------------------------")


def main() -> None:
    print("INVENTORY MANAGEMENT SYSTEM - LAB 8")

    try:
        inventory = create_oop_inventory()
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Unable to load inventory: {error}")
        return

    while True:
        show_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all_products()

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            remove_product(inventory)

        elif option == "6":
            save_inventory(inventory)

        elif option == "7":
            save_inventory(inventory)
            print("Program terminated.")
            break

        else:
            print("Invalid option. Choose 1 to 7.")


if __name__ == "__main__":
    main()
