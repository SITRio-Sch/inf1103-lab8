from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("An order line needs a Product object.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"Product ID: {self.__product.get_product_id()}")
        print(f"Name: {self.__product.name}")
        print(f"Unit Price: ${self.__product.price:.2f}")
        print(f"Quantity: {self.__quantity}")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
