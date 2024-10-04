from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

class TaskScheduler:
    def __init__(self, db_url):
        jobstores = {
            'default': SQLAlchemyJobStore(url=db_url)
        }
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    def start(self):
        self.scheduler.start()

    def add_job(self, func, trigger, **kwargs):
        return self.scheduler.add_job(func, trigger, **kwargs)

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def get_jobs(self):
        return self.scheduler.get_jobs()

# Uso:
# scheduler = TaskScheduler('sqlite:///jobs.sqlite')
# scheduler.start()
# scheduler.add_job(my_task, 'interval', hours=1)