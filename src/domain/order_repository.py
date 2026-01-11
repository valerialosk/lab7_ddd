from abc import ABC, abstractmethod
from src.domain.order import Order


class OrderRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Order:
        pass
    
    @abstractmethod
    def save(self, order: Order) -> None:
        pass
