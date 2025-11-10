# run_simulation.py

import time
import random
from collections import deque
from order_book_simulator import OrderBookSimulator # Import the simulator

# --- Configuration ---
NUM_EVENTS = 100000
PRICE_LEVEL = 100.00
PRICE_RANGE = 0.50

def generate_test_events(num_events: int) -> list:
    """Generates a list of random 'new order' or 'cancel' events."""
    events = []
    
    # Pre-seed the book with some orders
    for i in range(100):
        side = random.choice(['BUY', 'SELL'])
        price = PRICE_LEVEL + random.uniform(-PRICE_RANGE, PRICE_RANGE)
        quantity = random.randint(10, 100)
        events.append(('NEW', side, round(price, 2), quantity))
        
    for _ in range(num_events - 100):
        # 80% chance for a new order, 20% for a cancellation
        if random.random() < 0.8:
            side = random.choice(['BUY', 'SELL'])
            # Generate price near the market center
            price = PRICE_LEVEL + random.uniform(-PRICE_RANGE, PRICE_RANGE)
            quantity = random.randint(10, 100)
            events.append(('NEW', side, round(price, 2), quantity))
        else:
            events.append(('CANCEL', None, None, None))
            
    return events

def run_performance_test():
    """Executes the test events and measures performance metrics."""
    book = OrderBookSimulator()
    events = generate_test_events(NUM_EVENTS)
    
    total_new_orders = 0
    total_cancellations = 0
    orders_to_cancel = deque() # Store IDs of resting orders for cancellation
    
    print(f"Starting performance test with {NUM_EVENTS:,} events...")
    
    start_time = time.perf_counter()
    
    for event in events:
        event_type = event[0]
        
        if event_type == 'NEW':
            side, price, quantity = event[1], event[2], event[3]
            new_id = book.new_order(side, price, quantity)
            # Add successfully placed order ID to the cancellation queue
            if new_id in book.orders: 
                orders_to_cancel.append(new_id)
            total_new_orders += 1
            
        elif event_type == 'CANCEL':
            if orders_to_cancel:
                # Cancel one of the oldest placed orders
                id_to_cancel = orders_to_cancel.popleft() 
                if book.cancel_order(id_to_cancel):
                    total_cancellations += 1

    end_time = time.perf_counter()
    
    # --- Results Calculation ---
    total_time_s = end_time - start_time
    total_events_processed = total_new_orders + total_cancellations
    events_per_second = total_events_processed / total_time_s
    avg_latency_us = (total_time_s / total_events_processed) * 1_000_000 
    
    # --- Output Results ---
    print("\n" + "="*40)
    print("      PERFORMANCE TEST RESULTS      ")
    print("="*40)
    print(f"Total Events Processed: {total_events_processed:,}")
    print(f"  - New Orders:       {total_new_orders:,}")
    print(f"  - Cancellations:    {total_cancellations:,}")
    print(f"Total Trades Executed: {len(book.trade_log):,}")
    print(f"Total Execution Time: {total_time_s:.4f} seconds")
    print("----------------------------------------")
    print(f"Throughput: {events_per_second:,.0f} Events/second")
    print(f"Average Latency: {avg_latency_us:.2f} microseconds per event (μs)")
    print("="*40)

if __name__ == "__main__":
    run_performance_test()