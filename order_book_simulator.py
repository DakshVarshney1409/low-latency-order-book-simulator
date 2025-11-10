# order_book_simulator.py

from collections import deque
from typing import Dict, List, Union, Tuple
from order import Order # Import the Order class

class OrderBookSimulator:
    def __init__(self):
        # Bids: {Price: deque[Order]} 
        self.bids: Dict[float, deque[Order]] = {}
        # Asks: {Price: deque[Order]} 
        self.asks: Dict[float, deque[Order]] = {}
        
        # O(1) Lookup: {order_id: Order} - Crucial for fast cancellations/amendments
        self.orders: Dict[int, Order] = {}
        
        self.trade_log: List[Tuple[float, int, int, int]] = []
        self.next_order_id = 1

    # --- CORE LOGIC: NEW ORDER PROCESSING (MATCHING AND PLACEMENT) ---

    def new_order(self, side: str, price: float, quantity: int) -> int:
        """Processes a new limit order: matching phase followed by placement phase."""
        order_id = self.next_order_id
        self.next_order_id += 1
        
        incoming_order = Order(order_id, side, price, quantity)
        
        if side == 'BUY':
            resting_book, target_book, match_condition = self.asks, self.bids, lambda resting_p: incoming_order.price >= resting_p
            price_levels = sorted(resting_book.keys()) # Best Ask first (lowest price)
        else: # SELL
            resting_book, target_book, match_condition = self.bids, self.asks, lambda resting_p: incoming_order.price <= resting_p
            price_levels = sorted(resting_book.keys(), reverse=True) # Best Bid first (highest price)

        # PHASE 1: Matching
        for resting_price in price_levels:
            if incoming_order.quantity <= 0 or not match_condition(resting_price):
                break
                
            price_level = resting_book.get(resting_price)
            if not price_level: continue
            
            while price_level and incoming_order.quantity > 0:
                resting_order = price_level[0] 
                trade_qty = min(incoming_order.quantity, resting_order.quantity)
                
                # Trade Execution
                self.trade_log.append((resting_price, trade_qty, incoming_order.order_id, resting_order.order_id))
                
                # Update Quantities
                incoming_order.quantity -= trade_qty
                resting_order.quantity -= trade_qty
                
                # Handle Filled Resting Order
                if resting_order.quantity == 0:
                    price_level.popleft() 
                    del self.orders[resting_order.order_id]

            # Clean up empty price level
            if not price_level:
                del resting_book[resting_price]
        
        # PHASE 2: Book Placement
        if incoming_order.quantity > 0:
            self.orders[incoming_order.order_id] = incoming_order
            if incoming_order.price not in target_book:
                target_book[incoming_order.price] = deque()
                
            target_book[incoming_order.price].append(incoming_order)

        return order_id

    # --- CORE LOGIC: CANCEL ORDER (O(1) average time) ---
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancels an order by ID."""
        if order_id not in self.orders:
            return False

        order_to_cancel = self.orders[order_id]
        side = order_to_cancel.side
        price = order_to_cancel.price
        
        target_book = self.bids if side == 'BUY' else self.asks
        
        try:
            # O(N) bottleneck in Python's deque, but necessary here without custom data structures
            target_book[price].remove(order_to_cancel)
        except ValueError:
            return False

        del self.orders[order_id]
        
        if not target_book[price]:
            del target_book[price]
        
        return True

    def get_resting_order_ids(self) -> List[int]:
        """Helper to get IDs of orders currently in the book."""
        return list(self.orders.keys())
    
    def display_book(self):
        """Prints the current state of the order book, sorted correctly."""
        print("\n--- ASK SIDE (Sellers) ---")
        ask_prices = sorted(self.asks.keys())
        for price in ask_prices:
            qty = sum(o.quantity for o in self.asks[price])
            print(f"  ASK: ${price:.2f} | Qty: {qty} | ({len(self.asks[price])} orders)")

        print("--------------------------")
        bid_prices = sorted(self.bids.keys(), reverse=True)
        for price in bid_prices:
            qty = sum(o.quantity for o in self.bids[price])
            print(f"  BID: ${price:.2f} | Qty: {qty} | ({len(self.bids[price])} orders)")
        print("--- BID SIDE (Buyers) ---")