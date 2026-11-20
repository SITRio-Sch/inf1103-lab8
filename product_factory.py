from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """One place that knows every concrete product class.

    The rest of the program only asks for a product by type string and gets
    back a Product. Adding a new product type means editing this factory only,
    not every creation site (Factory pattern).
    """

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        # Convert first so bad values raise ValueError, not TypeError.
        try:
            price = float(price)
            stock = int(stock)
            weight = float(weight)
            download_size = float(download_size)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid product values for {product_id}.")

        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, weight, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
