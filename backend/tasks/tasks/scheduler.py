import dramatiq
import os
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from tasks.jobs import check_ssl_for_all_domain_names

from datetime import datetime


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(
        func=check_ssl_for_all_domain_names.send,
        trigger=CronTrigger.from_crontab(os.environ['CHECK_CRON_SCHEDULE']),
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
