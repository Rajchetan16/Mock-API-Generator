import threading
import time
import random
from collections import deque

# --- 1. Event Log Queue (The Core DSA: Thread-Safe FIFO) ---
class EventLogQueue:
    """
    A thread-safe Queue implementation for our log system.
    """
    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()
        # threading.Event is used to signal other threads to stop
        self.stop_requested = threading.Event() 

    def enqueue(self, event):
        """Adds a new event to the right side of the queue (FIFO)."""
        with self.lock:
            self.queue.append(event)
            # Optional: print for demonstration
            print(f"[{threading.current_thread().name}] ENQUEUED: {event['id']}")

    def dequeue(self):
        """Removes and returns the oldest event from the left side (FIFO)."""
        with self.lock:
            if not self.queue:
                return None
            return self.queue.popleft()

    def is_empty(self):
        """Checks if the queue is empty."""
        with self.lock:
            return not self.queue
            
    def stop(self):
        """Signals all processes to shut down gracefully."""
        self.stop_requested.set()


# --- 2. Event Generator (The Producer Thread) ---
class EventGenerator(threading.Thread):
    """Simulates a system producing log events and adding them to the queue."""
    def __init__(self, queue, max_events=20):
        # Name the thread for clear output
        super().__init__(name="EventGenerator") 
        self.queue = queue
        self.max_events = max_events

    def run(self):
        print(f"[{self.name}] Started generating events.")
        for i in range(1, self.max_events + 1):
            if self.queue.stop_requested.is_set():
                break

            event = {'id': i, 'details': f"Log event {i}.", 'arrival_time': time.time()}
            self.queue.enqueue(event)

            # Simulate variable arrival time for logs
            time.sleep(random.uniform(0.1, 0.5))

        print(f"\n[{self.name}] Finished generating {self.max_events} events.")


# --- 3. Log Processor (The Consumer Thread) ---
class LogProcessor(threading.Thread):
    """Simulates a system processing log events from the queue in order."""
    def __init__(self, queue):
        # Name the thread for clear output
        super().__init__(name="LogProcessor") 
        self.queue = queue
        self.processed_count = 0

    def run(self):
        print(f"[{self.name}] Started processing events.")
        
        while True:
            event = self.queue.dequeue()
            
            if event is not None:
                self.processed_count += 1
                # Simulate processing time to show concurrency
                time.sleep(random.uniform(0.05, 0.2))

                print(f"[{self.name}] PROCESSED: ID={event['id']} (Queue Size: {self.queue.queue.__len__()})")

            # Check if processing should stop: 
            # 1. Generator is finished AND 2. Queue is completely empty AND 3. Stop signal received
            if self.queue.stop_requested.is_set() and self.queue.is_empty():
                 break
            
            # If the queue is empty but generator might still be running, wait a little
            if event is None:
                time.sleep(0.1) 
        
        print(f"\n[{self.name}] Finished processing. Total processed: {self.processed_count}")


# --- 4. Main Execution Logic ---
def main(num_events=15):
    """Sets up and runs the Event Logging System."""
    print("--- Real-Time Event Logging System Simulation ---")

    # 1. Initialize the shared queue
    event_queue = EventLogQueue()

    # 2. Initialize the producer and consumer threads
    generator_thread = EventGenerator(event_queue, max_events=num_events)
    processor_thread = LogProcessor(event_queue)

    # 3. Start the threads
    generator_thread.start()
    processor_thread.start()

    # 4. Wait for the generator to finish (Producer side)
    generator_thread.join()

    # 5. Signal the system to stop once all events are generated 
    # and give the processor a few moments to finish its work
    print("\n[MAIN] Generator finished. Signalling graceful shutdown.")
    event_queue.stop()
    
    # 6. Wait for the processor to finish cleaning up the queue (Consumer side)
    processor_thread.join()

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    main(num_events=15)