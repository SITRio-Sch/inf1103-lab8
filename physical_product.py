from product import Product, ProductData
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        weight: float,
        supplier: Supplier
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print("Type: Physical")
        print(f"Weight: {self.__weight} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print("----------------------")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 5

    def to_dict(self) -> ProductData:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
