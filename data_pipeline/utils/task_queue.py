import redis
from rq import Queue

class TaskQueue:
    def __init__(self, name='default', host='localhost', port=6379, db=0):
        self.redis_conn = redis.Redis(host=host, port=port, db=db)
        self.queue = Queue(name, connection=self.redis_conn)

    def enqueue(self, func, *args, **kwargs):
        return self.queue.enqueue(func, *args, **kwargs)

    def get_job(self, job_id):
        return self.queue.fetch_job(job_id)

# Uso:
# task_queue = TaskQueue()
# job = task_queue.enqueue(expensive_operation, 10, 20)
# result = job.result