import time
from functools import wraps

def retry(exceptions, tries=4, delay=3, backoff=2, logger=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    msg = f"{str(e)}, Retrying in {mdelay} seconds..."
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Uso:
# @retry(exceptions=(RequestException, ConnectionError), tries=3, delay=1, backoff=2)
# def make_api_call():
#     # Código que pode falhar