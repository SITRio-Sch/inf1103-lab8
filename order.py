from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        if not order_id:
            raise ValueError("Order ID cannot be empty.")

        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        # A tuple copy: callers can read the lines but cannot add or remove them.
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates its own OrderLine, so outside code never hands one in.
        line = OrderLine(product, quantity)
        self.__order_lines.append(line)
        print("Order line added.")

    def remove_order_line(self, product_id: str) -> bool:
        for index, line in enumerate(self.__order_lines):
            if line.product.get_product_id() == product_id:
                del self.__order_lines[index]
                print("Order line removed.")
                return True

        print("Order line not found.")
        return False

    def calculate_total(self) -> float:
        total = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print(f"Order ID: {self.__order_id}")
        if len(self.__order_lines) == 0:
            print("Order is empty.")
        else:
            for line in self.__order_lines:
                line.display_information()
                print("----------------------")
        print(f"Order Total: ${self.calculate_total():.2f}")
