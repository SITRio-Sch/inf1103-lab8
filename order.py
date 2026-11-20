from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        if not order_id:
            raise ValueError("Order ID cannot be empty.")
        if discount is not None and not isinstance(discount, DiscountStrategy):
            raise TypeError("Discount must be a DiscountStrategy object.")

        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        # Order never decides which discount to use; it only holds a strategy.
        # The client supplies one, or the default NoDiscount is used.
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        # A tuple copy: callers can read the lines but cannot add or remove them.
        return tuple(self.__order_lines)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the discount behaviour without changing Order itself."""
        if not isinstance(discount, DiscountStrategy):
            raise TypeError("Discount must be a DiscountStrategy object.")
        self.__discount = discount

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
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        # No if/elif here: the discount behaviour lives in the strategy object.
        return self.__discount.apply(total)

    def display_order(self) -> None:
        print(f"Order ID: {self.__order_id}")
        if len(self.__order_lines) == 0:
            print("Order is empty.")
        else:
            for line in self.__order_lines:
                line.display_information()
                print("----------------------")
        print(f"Order Total: ${self.calculate_total():.2f}")
