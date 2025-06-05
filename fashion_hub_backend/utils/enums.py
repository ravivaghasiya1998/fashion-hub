from enum import auto
from strenum import StrEnum

class CategoryName(StrEnum):
    MEN = auto()
    WOMEN = auto()
    KIDS = auto()
    ACCESSORIES = auto()
    ELECTRIC = auto()
    KITCHEN = auto()

class OrderStatus(StrEnum):
    PENDING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class PaymentStatus(StrEnum):
    PENDING = auto()
    SUCCESS = auto()
    FAILED = auto()
    CANCELLED = auto()

class PaymentMethod(StrEnum):
    CREDIT_CARD = auto()
    DEBIT_CARD = auto()
    PAYPAL = auto()
    BANK_TRANSFER = auto()
    COD = auto()