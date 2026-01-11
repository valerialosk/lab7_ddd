import pytest
from decimal import Decimal
from src.domain.order import Order
from src.domain.order_line import OrderLine
from src.domain.money import Money
from src.domain.order_status import OrderStatus
from src.application.pay_order_use_case import PayOrderUseCase
from src.infrastructure.in_memory_order_repository import InMemoryOrderRepository
from src.infrastructure.fake_payment_gateway import FakePaymentGateway


class TestPayOrderUseCase:
    def test_successful_payment_of_valid_order(self):
        repository = InMemoryOrderRepository()
        gateway = FakePaymentGateway(should_succeed=True)
        use_case = PayOrderUseCase(repository, gateway)
        
        order = Order("order-1")
        order.add_line(OrderLine("Product A", 2, Money(Decimal("100"), "RUB")))
        order.add_line(OrderLine("Product B", 1, Money(Decimal("150"), "RUB")))
        repository.save(order)
        
        result = use_case.execute("order-1")
        
        saved_order = repository.get_by_id("order-1")
        assert result is True
        assert saved_order.status == OrderStatus.PAID
        assert saved_order.total() == Money(Decimal("350"), "RUB")
        charged_orders = gateway.get_charged_orders()
        assert len(charged_orders) == 1
        assert charged_orders[0][0] == "order-1"
        assert charged_orders[0][1] == Money(Decimal("350"), "RUB")
    
    def test_cannot_pay_empty_order(self):
        repository = InMemoryOrderRepository()
        gateway = FakePaymentGateway(should_succeed=True)
        use_case = PayOrderUseCase(repository, gateway)
        
        order = Order("order-2")
        repository.save(order)
        
        with pytest.raises(ValueError, match="Cannot pay empty order"):
            use_case.execute("order-2")
        
        # статус остался PENDING
        saved_order = repository.get_by_id("order-2")
        assert saved_order.status == OrderStatus.PENDING
    
    def test_cannot_pay_order_twice(self):
        repository = InMemoryOrderRepository()
        gateway = FakePaymentGateway(should_succeed=True)
        use_case = PayOrderUseCase(repository, gateway)
        
        order = Order("order-3")
        order.add_line(OrderLine("Product C", 1, Money(Decimal("200"), "RUB")))
        repository.save(order)
        
        # первая оплата успешна
        use_case.execute("order-3")
        
        # вторая оплата вызывает ошибку
        with pytest.raises(ValueError, match="Order is already paid"):
            use_case.execute("order-3")
    
    def test_cannot_modify_order_after_payment(self):
        repository = InMemoryOrderRepository()
        gateway = FakePaymentGateway(should_succeed=True)
        use_case = PayOrderUseCase(repository, gateway)
        
        order = Order("order-4")
        order.add_line(OrderLine("Product D", 1, Money(Decimal("300"), "RUB")))
        repository.save(order)
        
        use_case.execute("order-4")
        
        # после оплаты нельзя добавлять строки
        paid_order = repository.get_by_id("order-4")
        with pytest.raises(ValueError, match="Cannot modify paid order"):
            paid_order.add_line(OrderLine("Product E", 1, Money(Decimal("100"), "RUB")))
    
    def test_correct_total_calculation(self):
        order = Order("order-5")
        
        order.add_line(OrderLine("Product F", 3, Money(Decimal("50"), "RUB")))
        order.add_line(OrderLine("Product G", 2, Money(Decimal("75"), "RUB")))
        order.add_line(OrderLine("Product H", 1, Money(Decimal("200"), "RUB")))
        
        total = order.total()
        expected_total = Money(Decimal("500"), "RUB")
        assert total == expected_total
        
        # итог равен сумме строк
        manual_sum = (
            order.lines[0].subtotal() +
            order.lines[1].subtotal() +
            order.lines[2].subtotal()
        )
        assert total == manual_sum
