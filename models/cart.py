class CartItem:
    def __init__(self, cart_id: int, buyer_id: int, product_id: int, product_name: str, quantity: int, price: float):
        self.cart_id = cart_id
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    @property
    def total(self) -> float:
        """Calculate total price for this cart item."""
        return self.price * self.quantity
