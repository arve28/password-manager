import time


def measure_time(func):
    def wrapper(*_args):
        start_time = time.time()
        func(*_args)
        end_time = time.time()
        print(f"{func.__qualname__} completed in {end_time - start_time:.2f} seconds")
    return wrapper
