"""
Core Producer-Consumer Logic Implementation
-------------------------------------------
This module demonstrates the thread-safe buffering mechanism refactored 
to handle high-frequency IoT sensor bursts.

Author: Boyi Zhang
"""

import threading
import queue
import time
import logging

# Configuration for simulation
MAX_QUEUE_SIZE = 1000
SERIAL_PORT = '/dev/ttyACM0'

# Thread-safe buffer acting as the shock absorber
data_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)

def producer_serial_reader():
    """
    The Producer: Continuously reads raw bytes from hardware.
    Running as a daemon thread to unblock the main process.
    """
    logging.info(f"Starting serial listener on {SERIAL_PORT}...")
    
    # Context manager for resource handling (Pseudo-code for hardware connection)
    # with serial.Serial(SERIAL_PORT, 9600) as ser:
    while True:
        try:
            # Simulated blocking read from hardware
            # raw_data = ser.readline()
            
            # In simulation, we assume raw_data is received
            raw_data = {"sensor_id": 1, "temp": 24.5, "status": "occupied"}
            
            # Non-blocking put with timeout handling to prevent deadlocks
            data_queue.put(raw_data, timeout=1)
            
        except queue.Full:
            logging.warning("QUEUE OVERFLOW PROTECTION: Dropping oldest packet")
            # Strategy: Drop old data to keep system live, or log error
        except Exception as e:
            logging.error(f"Hardware Interface Error: {e}")

def consumer_db_writer():
    """
    The Consumer: Pulls data from the buffer and commits to DB.
    Optimized with batch processing.
    """
    batch_buffer = []
    BATCH_SIZE = 50
    
    logging.info("Starting Database Consumer Worker...")
    
    while True:
        item = data_queue.get()
        if item is None: break  # Sentinel to stop thread
        
        batch_buffer.append(item)
        
        # Batch write optimization
        if len(batch_buffer) >= BATCH_SIZE:
            _flush_to_database(batch_buffer)
            batch_buffer.clear()
        
        data_queue.task_done()

def _flush_to_database(batch):
    """
    Helper function to handle transaction management.
    """
    # with db_session_scope() as session:
    #     session.bulk_save_objects(batch)
    print(f"Committed {len(batch)} records to MySQL.")

# Main entry point for the backend service
if __name__ == "__main__":
    # Initialize threads
    t_producer = threading.Thread(target=producer_serial_reader, daemon=True)
    t_consumer = threading.Thread(target=consumer_db_writer)
    
    t_producer.start()
    t_consumer.start()
    
    t_consumer.join()
