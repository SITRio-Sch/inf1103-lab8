import csv
import json
import os

from discount_strategy import BulkDiscount, PercentageDiscount
from inventory import Inventory
from order import Order
from product import ProductData
from product_factory import ProductFactory
from supplier import Supplier

INVENTORY_FILE = "inventory.json"
PRODUCTS_FILE = "products.csv"

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

        # Section 1.5 fix: creation goes through the factory, so this loop
        # knows only about Product, not about the concrete classes.
        product = ProductFactory.create(
            product_type,
            str(item["id"]),
            str(item["name"]),
            float(item["price"]),
            int(item["stock"]),
            supplier,
            float(item.get("weight", 0)),
            float(item.get("download_size", 0)),
        )

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


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user gives a positive number.

    float() raises ValueError for text like "abc"; the bad value itself is
    handled with validation (value <= 0), so both cases are covered here.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, st: Inventory, supplier: Supplier) -> None:
    """Read a CSV file and create one product per row, without crashing."""
    loaded = 0

    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"{path} not found.")
    else:
        with file:
            rows = list(csv.reader(file))

        # Read rows with csv.reader and skip the header row.
        for row in rows[1:]:
            try:
                product = ProductFactory.create(
                    row[0], row[1], row[2], row[3], row[4], supplier
                )
            except ValueError:
                # Report this row and keep going - one bad row does not stop the file.
                print(f"Skipped row: {row}")
                continue

            if st.add_product(product):
                loaded += 1

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")



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

    # get_positive_float loops on bad input instead of crashing.
    price = get_positive_float("Price: ")

    try:
        stock = int(input("Stock Quantity: "))

        if stock < 0:
            print("Stock cannot be negative.")
            return

        extra = float(input("Weight (kg) or Download Size (MB): "))

        if extra < 0:
            print("Extra value cannot be negative.")
            return

        # The factory decides which concrete class to build.
        product = ProductFactory.create(
            "physical" if product_type == "1" else "digital",
            product_id,
            name,
            price,
            stock,
            supplier,
            extra,
            extra,
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


def apply_discount_example(inventory: Inventory) -> None:
    """Small demo: one order, discount behaviour swapped through strategies."""
    print("\nDiscount Example")

    product_id = input("Enter Product ID to order: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    quantity = int(get_positive_float("Quantity: "))

    order = None
    order_total_before: float | None = None

    try:
        order = Order(order_id="ORD-001")
        order.add_order_line(product, quantity)
        order_total_before = order.calculate_total()
        print(f"Total with no discount: ${order_total_before:.2f}")

        percent = int(input("Percent discount (0 to skip): "))
        if percent > 0:
            order.set_discount(PercentageDiscount(percent))
            print(f"Total with percentage: ${order.calculate_total():.2f}")

        # Bulk discount applies at a threshold of 200.
        if order_total_before >= 200:
            order.set_discount(BulkDiscount(200, 20))
            print(f"Total with bulk discount: ${order.calculate_total():.2f}")
    except (ValueError, TypeError) as error:
        print(f"Discount example failed: {error}")


def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Save Inventory")
    print("7. Load Products from CSV")
    print("8. Discount Example (Strategy)")
    print("9. Exit")
    print("----------------------------")


def main() -> None:
    print("INVENTORY MANAGEMENT SYSTEM - LAB 9")

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
            load_products(PRODUCTS_FILE, inventory, DEFAULT_SUPPLIER)

        elif option == "8":
            apply_discount_example(inventory)

        elif option == "9":
            save_inventory(inventory)
            print("Program terminated.")
            break

        else:
            print("Invalid option. Choose 1 to 9.")


if __name__ == "__main__":
    main()
