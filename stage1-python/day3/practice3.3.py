import random
from functools import wraps

def retry(max_attempts=3):          
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        break
            raise last_exception      
        return wrapper
    return decorator

@retry(max_attempts=3)            
def flaky_request():
    if random.random() < 0.7:
        raise ConnectionError("网络错误!")
    return "请求成功"

# 测试
for _ in range(5):
    try:
        print(flaky_request())
    except ConnectionError as e:
        print(f"最终失败: {e}")
    print("-" * 30)