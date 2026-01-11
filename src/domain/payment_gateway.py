from abc import ABC, abstractmethod
from src.domain.money import Money


class PaymentGateway(ABC):
    
    @abstractmethod
    def charge(self, order_id: str, money: Money) -> bool:
        pass
