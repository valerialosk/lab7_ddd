from src.domain.order_repository import OrderRepository
from src.domain.payment_gateway import PaymentGateway


class PayOrderUseCase:
    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self._order_repository = order_repository
        self._payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> bool:
        # 1. загружаем заказ из репозитория
        order = self._order_repository.get_by_id(order_id)
        
        # 2. выполняем доменную операцию (проверяются инварианты)
        order.pay()
        
        # 3. вызываем платёж через gateway
        total = order.total()
        payment_success = self._payment_gateway.charge(order_id, total)
        
        if not payment_success:
            raise ValueError("Payment failed")
        
        # 4. сохраняем заказ
        self._order_repository.save(order)
        
        # 5. возвращаем результат
        return True
