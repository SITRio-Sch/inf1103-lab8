from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")

        if self.find_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return False

        self.__products.append(product)
        print("Product added successfully.")
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def remove_product(self, product_id: str) -> Product | None:
        # Removes only the reference from this inventory. The product object
        # itself lives on and can still be used or added to another inventory.
        for index, product in enumerate(self.__products):
            if product.get_product_id() == product_id:
                del self.__products[index]
                print("Product removed from inventory.")
                return product

        print("Product not found.")
        return None

    def display_all_products(self) -> None:
        if len(self.__products) == 0:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()

    def get_products(self) -> list[Product]:
        return self.__products.copy()
