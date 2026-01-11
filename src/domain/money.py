from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "RUB"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency cannot be empty")
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError(f"Cannot add different currencies: {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    def __gt__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare different currencies: {self.currency} and {other.currency}")
        return self.amount > other.amount
    
    def __repr__(self) -> str:
        return f"Money({self.amount}, {self.currency})"
