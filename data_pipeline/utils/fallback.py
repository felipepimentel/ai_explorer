from functools import wraps
import time

def with_fallback(fallback_function, max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"All attempts failed. Using fallback function.")
                        return fallback_function(*args, **kwargs)
                    time.sleep(delay)
        return wrapper
    return decorator

# Uso:
# def fallback_embedding():
#     return [0] * 768  # Retorna um vetor de zeros como fallback
#
# @with_fallback(fallback_embedding)
# def generate_embedding(text):
#     # Código para gerar embedding