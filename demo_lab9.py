"""Runs the Lab 9 pieces and prints what actually happens (for the notes)."""

import io
import sys

from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from inventory_manager import get_positive_float, load_products
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    supplier = Supplier("S01", "Demo Supplier", "demo@example.com")
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier, 2.0)

    section("2.2/2.3 order of 250 with BulkDiscount(200, 20)")
    order = Order("ORD-1", BulkDiscount(200, 20))
    for _ in range(10):
        order.add_order_line(lamp, 1)
    print(f"calculate_total() = {order.calculate_total()}")

    section("2.2/2.3 same order with PercentageDiscount(10)")
    order.set_discount(PercentageDiscount(10))
    print(f"calculate_total() = {order.calculate_total()}")

    section("2.4 same order with StudentDiscount (5%, new class, Order unchanged)")
    order.set_discount(StudentDiscount())
    print(f"calculate_total() = {order.calculate_total()}")

    section("3.2 ProductFactory.create('service', ...)")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
    except ValueError as error:
        print(f"Caught ValueError: {error}")
    print("Program continues normally.")

    section("5.1 get_positive_float with abc, -5, 12.50")
    saved = sys.stdin
    sys.stdin = io.StringIO("abc\n-5\n12.50\n")
    try:
        value = get_positive_float("Price: ")
    finally:
        sys.stdin = saved
    print(f"returned {value}")

    section("5.2 load_products(products.csv)")
    inventory = Inventory()
    load_products("products.csv", inventory, supplier)
    print(f"inventory now holds: {sorted(p.get_product_id() for p in inventory.get_products())}")

    section("5.2 load_products on a missing file")
    load_products("nope.csv", Inventory(), supplier)


if __name__ == "__main__":
    main()
