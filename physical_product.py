from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight = weight

    def display_information(self):
        super().display_information()
        print("Type: Physical")
        print(f"Weight: {self.__weight} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print("----------------------")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.__weight * 5

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
