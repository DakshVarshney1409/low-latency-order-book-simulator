# Low-Latency Order Book Simulator

### Project Overview

This project implements a simplified, **single-threaded, ultra-low-latency Order Book Simulator** designed to efficiently process high volumes of buy and sell orders (Limit Orders) and execute trades based on **Price-Time Priority**.

The architecture is optimized to minimize overhead and avoid the unpredictable latency (jitter) associated with multi-threaded locking mechanisms, mirroring the design principles of real-world High-Frequency Trading (HFT) matching engines.

---

### Design Philosophy (Low Latency Focus)

The core goal was to achieve minimal, deterministic latency by leveraging efficient software architecture and data structures:

* **Single-Threaded Core:** The entire matching logic runs sequentially to guarantee strict time-ordering and **eliminate all lock contention**.
* **O(1) Lookups:** A Python `dict` (Hash Map) is used to track individual orders, ensuring $O(1)$ average-time complexity for finding and canceling orders by ID.
* **Time Priority Queue:** Python's built-in **`deque`** (double-ended queue) is used within each price level to ensure $O(1)$ insertion and $O(1)$ removal of the oldest order for trade execution.
* **Price Priority:** Price levels are maintained by sorting dictionary keys, ensuring trades always execute against the best available price first. 

---

### Project Structure

The code is organized into three separate Python files for clean modularity:

| File Name | Description |
| :--- | :--- |
| `order.py` | Defines the fundamental `Order` data class. |
| `order_book_simulator.py` | Contains the `OrderBookSimulator` class and all core operational logic: `new_order()`, `cancel_order()`, and matching procedures. |
| `run_simulation.py` | Contains the **performance testing harness**, randomized event generation, and throughput calculation logic. |

---

### Installation and Setup

This project requires only standard Python libraries and runs on Python 3.x.

1.  **Save Files:** Ensure the three files (`order.py`, `order_book_simulator.py`, `run_simulation.py`) are saved in the **same directory**.
2.  **Execute the script:** Run the simulation script from your terminal:

```bash
python run_simulation.py
```
