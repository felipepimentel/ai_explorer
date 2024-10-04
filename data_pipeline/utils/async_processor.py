import asyncio
from concurrent.futures import ProcessPoolExecutor

class AsyncProcessor:
    def __init__(self, max_workers=None):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
        self.loop = asyncio.get_event_loop()

    async def process_async(self, func, *args, **kwargs):
        return await self.loop.run_in_executor(self.executor, func, *args, **kwargs)

    async def process_batch_async(self, func, iterable):
        tasks = [self.process_async(func, item) for item in iterable]
        return await asyncio.gather(*tasks)

# Uso:
# async_processor = AsyncProcessor()
# result = await async_processor.process_async(expensive_function, arg1, arg2)
# batch_results = await async_processor.process_batch_async(expensive_function, [item1, item2, item3])