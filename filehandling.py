# -*- coding: utf-8 -*-
"""Filehandling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZEMJbCxDMWwndN3LEKYJ7Qy3AWiFpL0F
"""



"""#1 Discuss the scenarios where multithreading is preferable to multiprocessing and scenarios where multiprocessing is a better choice.




Multithreading is preferable to multiprocessing because:

Lower memory overhead: Threads share the same memory space, making them lightweight compared to processes.
Faster context switching: Switching between threads is quicker than processes since they share resources.
Efficient for I/O-bound tasks: Threads excel in handling tasks that wait for input/output, reducing idle CPU time.
Simpler inter-thread communication: Threads can easily share data through shared memory, avoiding the need for inter-process communication mechanisms.

#2. Describe what a process pool is and how it helps in managing multiple processes efficiently.


pool allows us to do multiple works in a process which make easier to parallelize the program.
you can effectively manage multiple processes, improve performance, and simplify the implementation of parallel tasks.
the pool distributes the tasks to the available processors using a FIFO: First In First Out.


how it helps in managing multiple processes efficiently.
by distributting the work load in multiplrprocessor.
each task submitted to the process pool may be a different target function

# 3.Explain what multiprocessing is and why it is used in Python programs.

Multiprocessing in Python enables programs to run multiple processes simultaneously, allowing full use of multiple CPU cores. It is primarily used for CPU-bound tasks like heavy computations or data processing, where dividing the work among multiple processes can significantly boost performance. Each process operates independently with its own memory space, overcoming Python's Global Interpreter Lock (GIL) limitation, which restricts threads from executing Python bytecode in parallel. This makes multiprocessing ideal for tasks requiring parallel execution to improve efficiency.
"""

#4. Write a Python program using multithreading where one thread adds numbers to a list, and another thread removes numbers from the list.
#Implement a mechanism to avoid race conditions using threading.Lock
import threading
import time

def adding(numb, lock):
    for i in range(1, 11):  # Changed range to 1-10
        with lock:
            numb.append(i)
            print(f"Added: {i} -> List: {numb}")
        time.sleep(0.2)  # Increased sleep time for better sync with removal

def removing(numb, lock):
    for i in range(1, 11):  # Removing 10 elements (if available)
        time.sleep(0.3)  # Delay to allow adding before attempting to remove
        with lock:
            if numb:
                removed = numb.pop(0)
                print(f"Removed: {removed} -> List: {numb}")
            else:
                print("No elements to remove.")

if __name__ == "__main__":
    numb = []
    lock = threading.Lock()

    # Create threads for adding and removing numbers
    thread1 = threading.Thread(target=adding, args=(numb, lock))
    thread2 = threading.Thread(target=removing, args=(numb, lock))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Final List:", numb)

"""#5. Describe the methods and tools available in Python for safely sharing data between threads and processes.
Tools for Safely Sharing Data in Python:
1. For Threads:
threading.Lock: Ensures only one thread accesses shared data at a time to avoid race conditions.
threading.RLock: A reentrant lock for a single thread to lock multiple times.
threading.Event: Synchronizes threads by signaling an event.
threading.Condition: Allows threads to wait for certain conditions to be met.
queue.Queue: A thread-safe queue for exchanging data between threads.
2. For Processes:
multiprocessing.Queue: A process-safe queue for communication.
multiprocessing.Pipe: Enables two-way communication between processes.
multiprocessing.Manager: Creates shared objects like lists or dictionaries for safe access across processes.

#6. Discuss why it’s crucial to handle exceptions in concurrent programs and the techniques available for doing so.

Exception handling is crucial in concurrent programs because it helps ensure that the program runs smoothly and doesn't terminate unexpectedly due to errors. In concurrent environments, where multiple threads or processes run simultaneously, unhandled exceptions in one thread/process can impact the overall execution and stability.

By handling exceptions, you ensure that errors are properly managed, allowing the program to continue executing other tasks, log errors, or clean up resources. Exception handling prevents abrupt terminations and ensures that the program can reach the final block, even when errors occur during execution.
"""

#7. Create a program that uses a thread pool to calculate the factorial of numbers from 1 to 10 concurrently.
#Use concurrent.futures.ThreadPoolExecutor to manage the threads.
import concurrent.futures

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == "__main__":
    numbers = range(1, 11)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(factorial, numbers))

    for num, fact in zip(numbers, results):
        print(f"Factorial of {num} is {fact}")

#Create a Python program that uses multiprocessing.Pool to compute the square of numbers from 1 to 10 in parallel. Measure the time taken to perform this computation using a pool of different sizes (e.g., 2, 4, 8 processes).

import multiprocessing
import time

def square(x):
    return x * x

def main():
    numbers = range(1, 11)

    pool_sizes = [2, 4, 8]
    for size in pool_sizes:
        start_time = time.time()

        with multiprocessing.Pool(processes=size) as pool:
            results = pool.map(square, numbers)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Pool size {size}: Time taken = {elapsed_time:.3f} seconds")

if __name__ == "__main__":
    main()