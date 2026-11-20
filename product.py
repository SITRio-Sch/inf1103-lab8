from abc import ABC, abstractmethod

from supplier import Supplier

# The shape of one product as stored in inventory.json.
ProductData = dict[str, str | float | int | dict[str, str]]


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ) -> None:
        if not product_id or not name:
            raise ValueError("Product ID and name cannot be empty.")
        # Lab 9 validation: a rule is broken, so raise with a clear message.
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if not isinstance(supplier, Supplier):
            raise TypeError("Product must be created with a Supplier object.")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

        self.__stock = quantity
        print("Stock updated successfully.")

    def display_information(self) -> None:
        print(f"Product ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.name}")
        print(f"Supplier Email: {self.__supplier.contact_email}")

    def get_product_id(self) -> str:
        return self.__product_id

    def to_dict(self) -> ProductData:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict()
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
