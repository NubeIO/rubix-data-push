import _thread
import schedule
import time

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def job():
    print("get rubix-point-server histroy data from postgress")
    print("join and convert into json")
    print("send json to a server over HTTP")


def _start_schedule(delay):
    s = schedule.Scheduler()
    s.every(delay).seconds.do(job)
    while True:
        s.run_pending()
        time.sleep(1)


def start_schedule(delay):
    _thread.start_new_thread(_start_schedule, (delay,))
