from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        args_repr = ','.join(repr(a) for a in args)
        kwargs_repr = ','.join(f"{k}={v!r}" for k,v in kwargs.items())
        all_args = args_repr
        if kwargs_repr:
            all_args+=',' + kwargs_repr if args_repr else kwargs_repr
        print(f"[LOG] Calling {func.__name__} with args=({all_args})",end=' ')
        try:
            result = func(*args,**kwargs)
            print(f" -> returned {result!r}")
            return result
        except Exception as e:
            print(f" -> raised {type(e).__name__}: {e}")
            raise
    return wrapper
        

# 测试
@logger
def divide(a, b):
    return a / b

divide(10, 2)   
divide(10, 0)   
