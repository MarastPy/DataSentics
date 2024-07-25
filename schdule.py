from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

def job():
    now = datetime.datetime.now()
    print(f"Running scheduled task at {now}")

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour=12, minute=0)  # Schedule the job every day at noon

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass