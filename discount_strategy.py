from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """One way of working with an order total.

    Order depends on this abstract class only, so any discount behaviour can
    be swapped in without editing Order (Strategy pattern + OCP).
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Default behaviour: the total is returned unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Take a percentage off the total, e.g. PercentageDiscount(10) = 10% off."""

    def __init__(self, percent: float) -> None:
        if percent <= 0 or percent > 100:
            raise ValueError("Discount percent must be between 1 and 100.")

        self.__percent: float = percent

    @property
    def percent(self) -> float:
        return self.__percent

    def apply(self, total: float) -> float:
        return total * (1 - self.__percent / 100)


class BulkDiscount(DiscountStrategy):
    """Take a fixed amount off once the total reaches a threshold."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0 or amount <= 0:
            raise ValueError("Bulk threshold and amount must be greater than zero.")

        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total
