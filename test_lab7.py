import json
import tempfile
from pathlib import Path

import inventory_manager
from product import Product
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped


# Create test products
laptop = PhysicalProduct("P001", "Laptop", 1200, 15, 2.5)
mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, 0.2)
software = DigitalProduct("D001", "Antivirus", 50, 100, 500)

print("=== PHYSICAL PRODUCTS ===")
laptop.display_information()
mouse.display_information()

print("\n=== DIGITAL PRODUCT ===")
software.display_information()

print("\n=== FULFILMENT TEST ===")
print(laptop.get_fulfilment_info())
print(software.get_fulfilment_info())

print("\n=== SHIPPING TEST ===")
assert laptop.calculate_shipping_cost() == 12.5
assert mouse.calculate_shipping_cost() == 1.0
assert isinstance(laptop, CanBeShipped)
assert not isinstance(software, CanBeShipped)
print("PASS: Shipping calculations and interface.")

print("\n=== ABSTRACT CLASS TEST ===")
try:
    Product("P003", "Test", 10, 5)
    raise AssertionError("Product should be abstract.")
except TypeError:
    print("PASS: Cannot instantiate Product directly.")

print("\n=== INVENTORY TEST ===")
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(mouse)
inventory.add_product(software)

assert inventory.search_product("D001") is software
assert len(inventory.get_products()) == 3
print("PASS: Inventory operations.")

print("\n=== JSON PERSISTENCE TEST ===")
original_file = inventory_manager.INVENTORY_FILE

try:
    with tempfile.TemporaryDirectory() as temp_folder:
        inventory_manager.INVENTORY_FILE = str(
            Path(temp_folder) / "inventory.json"
        )

        inventory_manager.save_inventory(inventory)
        loaded = inventory_manager.create_oop_inventory()

        assert isinstance(loaded.search_product("P001"), PhysicalProduct)
        assert isinstance(loaded.search_product("D001"), DigitalProduct)

        with open(inventory_manager.INVENTORY_FILE, "r") as file:
            saved = json.load(file)

        assert saved[0]["weight"] == 2.5
        assert saved[2]["download_size"] == 500

    print("PASS: JSON saves and restores both product types.")

finally:
    inventory_manager.INVENTORY_FILE = original_file

print("\nALL TESTS PASSED")
