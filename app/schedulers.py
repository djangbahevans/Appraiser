# IMPORT DEPENDENCIES
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.database import SQLALCHEMY_DATABASE_URL
import pytz

# DEFINE INSTANCES
jobstores = {'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL or 'sqlite:///./asset_store.db')}
executors = {'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = {'coalesce': False, 'max_instances': 3}

# DEFINE JOB SCHEDULER
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc, misfire_grace_time=60)
