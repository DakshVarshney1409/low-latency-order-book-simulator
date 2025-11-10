class Order:
    """Represents a single limit order in the book."""
    def __init__(self, order_id: int, side: str, price: float, quantity: int):
        self.order_id = order_id
        self.side = side  # 'BUY' or 'SELL'
        self.price = price
        self.quantity = quantity
        # Note: Time priority is implicit via placement in the deque

    def __repr__(self):
        return f"Order({self.order_id}, {self.side}, ${self.price:.2f}, Qty: {self.quantity})"