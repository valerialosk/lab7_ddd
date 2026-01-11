from typing import List
from src.domain.order_line import OrderLine
from src.domain.money import Money
from src.domain.order_status import OrderStatus
from decimal import Decimal


class Order:
    def __init__(self, order_id: str):
        if not order_id:
            raise ValueError("Order ID cannot be empty")
        
        self._order_id = order_id
        self._lines: List[OrderLine] = []
        self._status = OrderStatus.PENDING
    
    @property
    def order_id(self) -> str:
        return self._order_id
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    @property
    def lines(self) -> List[OrderLine]:
        return self._lines.copy()
    
    def add_line(self, line: OrderLine) -> None:
        if self._status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self._lines.append(line)
    
    def total(self) -> Money:
        if not self._lines:
            return Money(Decimal("0"), "RUB")
        
        total = self._lines[0].subtotal()
        for line in self._lines[1:]:
            total = total + line.subtotal()
        return total
    
    def pay(self) -> None:
        if not self._lines:
            raise ValueError("Cannot pay empty order")
        
        if self._status == OrderStatus.PAID:
            raise ValueError("Order is already paid")
        
        self._status = OrderStatus.PAID
