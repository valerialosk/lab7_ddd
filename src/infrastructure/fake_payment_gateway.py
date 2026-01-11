from src.domain.money import Money
from src.domain.payment_gateway import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_succeed: bool = True):
        self._should_succeed = should_succeed
        self._charged_orders = []
    
    def charge(self, order_id: str, money: Money) -> bool:
        if self._should_succeed:
            self._charged_orders.append((order_id, money))
            return True
        return False
    
    def get_charged_orders(self):
        return self._charged_orders.copy()
