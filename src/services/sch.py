import _thread
import schedule
import time

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def job():
    print("I'm working...")


def _startSchedule(delay):
    print(22222)
    s = schedule.Scheduler()
    s.every(delay).seconds.do(job)
    while True:
        s.run_pending()
        time.sleep(1)


def startSchedule(delay):
    _thread.start_new_thread(_startSchedule, (delay,))

# def job():
#     print("I'm working...")
#
# schedule.every(10).seconds.do(job)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
