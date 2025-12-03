from enum import Enum


class OrderStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderItem:
    def __init__(
        self,
        order_id: int,
        buyer_id: int,
        product_id: int,
        product_name: str,
        quantity: int,
        total_amount: float,
        delivery_address: str,
        status: OrderStatus = OrderStatus.CONFIRMED,
    ):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.total_amount = total_amount
        self.delivery_address = delivery_address
        self.status = status
