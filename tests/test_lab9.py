"""Automated tests for the Lab 9 Inventory Management System.

Run with: python -m pytest -q tests
"""

import pytest

from discount_strategy import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_manager import get_non_negative_int, get_positive_float, load_products
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S01", "Test Supplier", "test@example.com")


def make_lamp(weight: float = 2.0) -> PhysicalProduct:
    return PhysicalProduct("P001", "Desk Lamp", 25.00, 10, weight, make_supplier())


class LoyaltyDiscount(DiscountStrategy):
    """A discount invented only inside this test file: Order must not change."""

    def apply(self, total: float) -> float:
        return total - 10 if total >= 100 else total


# --- Section 2: Strategy pattern -------------------------------------------


def test_no_discount_leaves_total_unchanged():
    order = Order("ORD-1")
    order.add_order_line(make_lamp(), 2)
    assert order.calculate_total() == 50.0
    assert isinstance(order.discount, NoDiscount)


def test_percentage_discount_applied():
    order = Order("ORD-1", PercentageDiscount(10))
    order.add_order_line(make_lamp(), 4)  # 100 total
    assert order.calculate_total() == pytest.approx(90.0)


def test_bulk_discount_applies_at_threshold():
    order = Order("ORD-1", BulkDiscount(200, 20))
    order.add_order_line(make_lamp(), 10)  # 250 total
    assert order.calculate_total() == pytest.approx(230.0)


def test_bulk_discount_ignores_small_totals():
    order = Order("ORD-1", BulkDiscount(200, 20))
    order.add_order_line(make_lamp(), 4)  # 100 total
    assert order.calculate_total() == pytest.approx(100.0)


def test_student_discount_five_percent():
    # The Section 2.4 fourth discount: a new subclass, Order untouched.
    order = Order("ORD-1", StudentDiscount())
    order.add_order_line(make_lamp(), 4)  # 100 total
    assert order.calculate_total() == pytest.approx(95.0)


def test_strategy_can_be_swapped():
    order = Order("ORD-1")
    order.add_order_line(make_lamp(), 4)
    order.set_discount(PercentageDiscount(50))
    assert order.calculate_total() == pytest.approx(50.0)
    order.set_discount(BulkDiscount(200, 20))
    assert order.calculate_total() == pytest.approx(100.0)


def test_new_strategy_needs_no_order_change():
    # A discount the project never had, defined only in this file: Order is unchanged.
    order = Order("ORD-1", LoyaltyDiscount())
    order.add_order_line(make_lamp(), 4)  # 100 total
    assert order.calculate_total() == pytest.approx(90.0)


def test_order_rejects_non_strategy():
    order = Order("ORD-1")
    with pytest.raises(TypeError):
        order.set_discount("10 percent off")  # type: ignore[arg-type]


# --- Section 3: Factory pattern --------------------------------------------


def test_factory_creates_both_product_types():
    supplier = make_supplier()
    physical = ProductFactory.create("physical", "P1", "Chair", 30.0, 4, supplier, 5.0)
    digital = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, supplier, 0.0, 250.0)

    assert isinstance(physical, PhysicalProduct)
    assert isinstance(digital, DigitalProduct)
    assert isinstance(physical, Product)  # callers only need the base type


def test_factory_raises_for_unknown_type():
    with pytest.raises(ValueError, match="Unknown product type: service"):
        ProductFactory.create("service", "S1", "Install", 30.0, 5, make_supplier())


def test_factory_bad_price_raises_value_error():
    with pytest.raises(ValueError):
        ProductFactory.create("physical", "P2", "Chair", "abc", 3, make_supplier())


# --- Section 4: Validation --------------------------------------------------


def test_order_line_rejects_bad_quantity():
    lamp = make_lamp()
    with pytest.raises(ValueError):
        OrderLine(lamp, 0)
    with pytest.raises(ValueError):
        OrderLine(lamp, -3)


def test_product_rejects_bad_price_and_stock():
    supplier = make_supplier()
    with pytest.raises(ValueError):
        PhysicalProduct("P1", "Lamp", 0.0, 5, 1.0, supplier)
    with pytest.raises(ValueError):
        PhysicalProduct("P1", "Lamp", -4.0, 5, 1.0, supplier)
    with pytest.raises(ValueError):
        DigitalProduct("D1", "Editor", 10.0, -1, 50.0, supplier)


def test_update_stock_rejects_negative_quantity():
    lamp = make_lamp()
    with pytest.raises(ValueError, match="Stock cannot be negative."):
        lamp.update_stock(-1)
    assert lamp.stock == 10


# --- Section 5: Exception handling ------------------------------------------


def test_get_positive_float_loops_until_valid(monkeypatch, capsys):
    answers = iter(["abc", "-5", "12.50"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert get_positive_float("Price: ") == 12.50

    printed = capsys.readouterr().out
    assert "Please enter a valid number, e.g. 12.50" in printed
    assert "Please enter a number greater than zero." in printed


def test_get_non_negative_int_reasks_until_valid(monkeypatch, capsys):
    answers = iter(["abc", "-2", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert get_non_negative_int("Stock Quantity: ") == 3

    printed = capsys.readouterr().out
    assert "Please enter a whole number, e.g. 10" in printed
    assert "Please enter a number that is zero or greater." in printed


def test_load_products_skips_bad_rows(tmp_path, capsys):
    csv_path = tmp_path / "products.csv"
    csv_path.write_text(
        "product_type,product_id,name,price,stock_quantity\n"
        "physical,P001,Desk Lamp,25.00,10\n"
        "digital,D001,Photo Editor,49.90,100\n"
        "service,S001,Installation,30.00,5\n"
        "physical,P002,Office Chair,abc,3\n"
        "physical,P003,Monitor Stand,39.50,7\n",
        encoding="utf-8",
    )

    inventory = Inventory()
    load_products(str(csv_path), inventory, make_supplier())

    ids = {product.get_product_id() for product in inventory.get_products()}
    assert ids == {"P001", "D001", "P003"}

    printed = capsys.readouterr().out
    assert "Skipped row:" in printed
    assert "3 products loaded." in printed
    assert "Load attempt finished." in printed


def test_load_products_missing_file_does_not_crash(tmp_path, capsys):
    inventory = Inventory()
    load_products(str(tmp_path / "nope.csv"), inventory, make_supplier())

    printed = capsys.readouterr().out
    assert "Products file not found:" in printed
    assert "Load attempt finished." in printed
    assert inventory.get_products() == []


# --- Order behaviour is unchanged in structure -----------------------------


def test_order_add_and_remove_lines():
    order = Order("ORD-2")
    order.add_order_line(make_lamp(), 2)
    assert len(order.order_lines) == 1
    assert order.remove_order_line("P001") is True
    assert order.calculate_total() == 0.0
