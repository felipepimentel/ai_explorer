import redis
import json
from functools import wraps

class DistributedCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value, expiration=None):
        self.redis.set(key, json.dumps(value), ex=expiration)

    def get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def delete(self, key):
        self.redis.delete(key)

def cached(cache, prefix='', expiration=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result, expiration)
            return result
        return wrapper
    return decorator

# Uso:
# cache = DistributedCache()
# @cached(cache, prefix='my_function', expiration=3600)
# def expensive_operation(x, y):
#     # Operação custosa
#     return x + y