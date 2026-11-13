import gc
import inspect
import os
import sys
import typing
import weakref
from collections.abc import Callable

# `python -I` ignores the script's own folder, so add it to the path first.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from digital_product import DigitalProduct  # noqa: E402
from inventory import Inventory  # noqa: E402
from order import Order  # noqa: E402
from order_line import OrderLine  # noqa: E402
from physical_product import PhysicalProduct  # noqa: E402
from product import Product  # noqa: E402
from supplier import Supplier  # noqa: E402


def section(title: str) -> None:
    print(f"\n==== {title} ====")


def assert_raises(
    error_type: type[Exception],
    func: Callable[..., object],
    *args: object
) -> None:
    try:
        func(*args)
    except error_type as error:
        print(f"PASS: {error_type.__name__} raised: {error}")
        return

    raise AssertionError(f"Expected {error_type.__name__} was not raised.")


def test_association() -> None:
    section("ASSOCIATION")

    supplier = Supplier("S100", "Test Supplier", "test@supplier.example")
    laptop = PhysicalProduct("T-LAP", "Test Laptop", 1000.0, 5, 2.0, supplier)
    ebook = DigitalProduct("T-BOOK", "Test Ebook", 20.0, 50, 10.0, supplier)

    print("-- Supplier shown through the laptop:")
    laptop.display_information()
    print("-- Supplier shown through the ebook:")
    ebook.display_information()

    assert laptop.supplier is supplier
    print("PASS: laptop.supplier is supplier")

    assert ebook.supplier is supplier
    print("PASS: ebook.supplier is supplier")

    assert laptop is not supplier and ebook is not supplier and laptop is not ebook
    print("PASS: products and supplier are separate objects")

    assert_raises(ValueError, Supplier, "", "No ID", "x@example.com")
    assert_raises(
        TypeError, PhysicalProduct, "T-BAD", "Bad", 1.0, 1, 1.0, "not a supplier"
    )

    print("PREDICT FIRST 1 CHECK: 'del supplier' removes only the name. "
          "Will both products still show the supplier?")
    del supplier

    laptop.display_information()
    ebook.display_information()
    assert laptop.supplier.name == "Test Supplier"
    assert ebook.supplier.name == "Test Supplier"
    print("PASS: supplier still reachable through both products after del")


def test_aggregation() -> None:
    section("AGGREGATION")

    mouse_supplier = Supplier("S101", "Mouse Co", "orders@mouse.example")
    # Created before any Inventory exists.
    mouse = PhysicalProduct("T-MOUSE", "Test Mouse", 25.0, 10, 0.1, mouse_supplier)

    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(mouse)
    removed = inventory_a.remove_product("T-MOUSE")
    assert removed is mouse
    print("PASS: remove_product returned the same object")

    assert inventory_a.find_product("T-MOUSE") is None
    print("PASS: inventory A no longer finds the mouse")

    print("-- Mouse still works after removal from A:")
    mouse.display_information()
    mouse.update_stock(7)
    assert mouse.stock == 7
    print("PASS: update_stock works with no inventory attached")

    inventory_b.add_product(mouse)
    assert inventory_b.find_product("T-MOUSE") is mouse
    print("PASS: inventory B finds the same mouse object")

    assert inventory_a.find_product("T-MOUSE") is None
    print("PASS: inventory A still finds nothing")

    inventory_b.remove_product("T-MOUSE")
    print("PREDICT FIRST 2 CHECK: inventory B is now empty. "
          "Does the mouse still display and update?")
    inventory_b.display_all_products()
    mouse.display_information()
    mouse.update_stock(8)
    assert mouse.stock == 8
    print("PASS: product still works after its inventory is emptied")


def test_composition() -> None:
    section("COMPOSITION")

    supplier = Supplier("S102", "Key Co", "sales@key.example")
    keyboard = PhysicalProduct("T-KEY", "Test Keyboard", 45.0, 25, 0.8, supplier)
    software = DigitalProduct("T-SOFT", "Test Software", 20.0, 50, 1.0, supplier)

    order_a = Order("ORD-A")
    order_a.add_order_line(keyboard, 2)   # 2 x 45.00 = 90.00
    order_a.add_order_line(software, 3)   # 3 x 20.00 = 60.00

    print("-- ORD-A contents:")
    order_a.display_order()

    assert len(order_a.order_lines) == 2
    total = order_a.calculate_total()
    assert abs(total - 150.0) < 0.001
    print(f"PASS: ORD-A total is {total:.2f}")

    order_b = Order("ORD-B")
    order_b.add_order_line(keyboard, 1)

    line_a = order_a.order_lines[0]
    line_b = order_b.order_lines[0]
    assert line_a is not line_b
    assert line_a.product is line_b.product is keyboard
    print("PASS: each order has its own OrderLine; both point at the same keyboard")

    assert isinstance(order_a.order_lines, tuple)
    print("PASS: order_lines is a tuple")

    try:
        order_a.order_lines.append(line_b)  # type: ignore[attr-defined]
    except AttributeError:
        print("PASS: lines cannot be appended to order_lines from outside")
    else:
        raise AssertionError("order_lines should not accept appends.")

    for name, member in inspect.getmembers(Order, predicate=inspect.isfunction):
        hints = typing.get_type_hints(member)
        assert OrderLine not in hints.values()
        print(f"PASS: Order.{name} takes no OrderLine")

    assert_raises(ValueError, order_a.add_order_line, keyboard, 0)
    assert_raises(ValueError, OrderLine, keyboard, 0)
    assert len(order_a.order_lines) == 2
    print("PASS: quantity 0 is rejected and ORD-A is unchanged")

    line_ref = weakref.ref(line_b)
    order_ref = weakref.ref(order_b)
    del line_b
    del order_b
    gc.collect()

    print("PREDICT FIRST 3 CHECK: after 'del order_b', are ORD-B and its line "
          "still reachable? Does the keyboard still exist?")
    assert order_ref() is None
    assert line_ref() is None
    print("PASS: ORD-B and its OrderLine are no longer reachable")

    keyboard.display_information()
    assert order_a.calculate_total() == total
    print("PASS: keyboard still exists and ORD-A is unchanged")


def process_products(products: list[Product]) -> list[str]:
    fulfilment: list[str] = []

    for product in products:
        product.update_stock(12)
        fulfilment.append(product.get_fulfilment_info())
        product.display_information()

    return fulfilment


def test_lsp() -> None:
    section("LSP")

    supplier = Supplier("S103", "Mixed Co", "info@mixed.example")
    chair = PhysicalProduct("T-CHAIR", "Test Chair", 80.0, 3, 12.0, supplier)
    ebook = DigitalProduct("T-EBOOK", "Test Ebook", 15.0, 9, 5.0, supplier)

    mixed: list[Product] = [chair, ebook]
    results = process_products(mixed)

    assert chair.stock == 12 and ebook.stock == 12
    print("PASS: update_stock worked on both physical and digital products")

    assert results[0] == "This product requires physical shipping."
    assert results[1] == "This product is delivered digitally."
    print("PASS: get_fulfilment_info gave the right answer for each type")

    assert "update_stock" not in DigitalProduct.__dict__
    print("PASS: DigitalProduct does not override update_stock")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_show_product_details() -> None:
    section("SHOW_PRODUCT_DETAILS (POLYMORPHISM)")

    supplier = Supplier("S104", "Detail Co", "hello@detail.example")
    lamp = PhysicalProduct("T-LAMP", "Test Lamp", 30.0, 4, 1.5, supplier)
    guide = DigitalProduct("T-GUIDE", "Test Guide", 9.0, 40, 2.0, supplier)

    show_product_details(lamp)
    show_product_details(guide)
    print("PASS: show_product_details ran on a PhysicalProduct and a DigitalProduct")


def test_shared_inventory_lsp() -> None:
    section("SHARED INVENTORY LSP")

    supplier = Supplier("S105", "Shared Co", "team@shared.example")
    desk = PhysicalProduct("T-DESK", "Test Desk", 150.0, 2, 20.0, supplier)
    course = DigitalProduct("T-COURSE", "Test Course", 60.0, 100, 500.0, supplier)

    inventory = Inventory()
    assert inventory.add_product(desk)
    assert inventory.add_product(course)

    fulfilment: list[str] = []
    for product in inventory.get_products():
        product.display_information()
        info = product.get_fulfilment_info()
        print(info)
        fulfilment.append(info)

    assert fulfilment == [
        "This product requires physical shipping.",
        "This product is delivered digitally.",
    ]
    print("PASS: one loop over the shared Inventory handled both product types")


def test_fulfilment_predictions() -> None:
    section("PREDICT FIRST 4")

    supplier = Supplier("S106", "Ship Co", "ship@example.com")
    box = PhysicalProduct("T-BOX", "Test Box", 5.0, 10, 0.5, supplier)
    pdf = DigitalProduct("T-PDF", "Test PDF", 3.0, 99, 0.2, supplier)

    print("PREDICT FIRST 4 CHECK: what does get_fulfilment_info() print "
          "for each product?")
    box_text = box.get_fulfilment_info()
    pdf_text = pdf.get_fulfilment_info()
    print(f"Physical: {box_text}")
    print(f"Digital: {pdf_text}")

    assert box_text == "This product requires physical shipping."
    assert pdf_text == "This product is delivered digitally."
    print("PASS: fulfilment text matches the implementation for both types")


def test_type_hints() -> None:
    section("TYPE HINTS")

    hints = typing.get_type_hints(Product.__init__)
    assert hints["supplier"] is Supplier
    print(f"PASS: Product.__init__ hints include supplier: {hints['supplier'].__name__}")

    methods: list[Callable[..., object]] = [
        Supplier.to_dict,
        Product.update_stock,
        Product.get_fulfilment_info,
        PhysicalProduct.calculate_shipping_cost,
        Inventory.add_product,
        Inventory.find_product,
        Inventory.remove_product,
        Inventory.display_all_products,
        Inventory.get_products,
        show_product_details,
        OrderLine.calculate_subtotal,
        Order.add_order_line,
        Order.remove_order_line,
        Order.calculate_total,
        Order.display_order,
    ]

    for method in methods:
        method_hints = typing.get_type_hints(method)
        assert "return" in method_hints
        assert typing.Any not in method_hints.values()
        print(f"PASS: {method.__qualname__} -> {method_hints}")


def main() -> None:
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_show_product_details()
    test_shared_inventory_lsp()
    test_fulfilment_predictions()
    test_type_hints()
    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    main()
