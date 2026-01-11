from typing import Dict
from src.domain.order import Order
from src.domain.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Order:
        if order_id not in self._orders:
            raise ValueError(f"Order with ID {order_id} not found")
        return self._orders[order_id]
    
    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order
