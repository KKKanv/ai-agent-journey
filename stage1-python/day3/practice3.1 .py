import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.perf_counter()
        result=func(*args,**kwargs)
        end=time.perf_counter()
        print(f"{func.__name__} took {end - start:.3f}s")
        return result
    return wrapper

@timer
def slow_add(n):
    total = 0
    for i in range(n):
        total += i
    return total

slow_add(10000000)