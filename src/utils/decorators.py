"""Decorator functions used in application."""
import time


def measure_time(func):
    """Measures function's running time."""
    def wrapper(*_args):
        start_time = time.time()
        func(*_args)
        end_time = time.time()
        print(f"{func.__qualname__} completed in {end_time - start_time:.2f} seconds")
    return wrapper
