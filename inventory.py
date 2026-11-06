from product import Product


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")

        if self.search_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return False

        self.__products.append(product)
        print("Product added successfully.")
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def display_all(self):
        if len(self.__products) == 0:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()

    def get_products(self):
        return self.__products.copy()
