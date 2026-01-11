from dataclasses import dataclass
from src.domain.money import Money


@dataclass
class OrderLine:
    product_name: str
    quantity: int
    price: Money
    
    def __post_init__(self):
        if not self.product_name:
            raise ValueError("Product name cannot be empty")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price.amount <= 0:
            raise ValueError("Price must be positive")
    
    def subtotal(self) -> Money:
        from decimal import Decimal
        return Money(self.price.amount * Decimal(self.quantity), self.price.currency)
