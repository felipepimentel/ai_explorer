import functools
from data_pipeline.utils.distributed_cache import DistributedCache

class CacheManager:
    def __init__(self, use_distributed=False):
        self.use_distributed = use_distributed
        self.local_cache = {}
        self.distributed_cache = DistributedCache() if use_distributed else None

    def cache(self, ttl=3600):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = f"{func.__name__}:{args}:{kwargs}"
                
                if self.use_distributed:
                    result = self.distributed_cache.get(key)
                    if result is None:
                        result = func(*args, **kwargs)
                        self.distributed_cache.set(key, result, ttl)
                else:
                    result = self.local_cache.get(key)
                    if result is None:
                        result = func(*args, **kwargs)
                        self.local_cache[key] = result
                
                return result
            return wrapper
        return decorator

cache_manager = CacheManager(use_distributed=config.USE_DISTRIBUTED_CACHE)

# Uso:
# @cache_manager.cache(ttl=3600)
# def expensive_operation(x, y):
#     # Operação custosa
#     return x + y