# coding:utf-8

from multiprocessing import Value, Queue, Process, Condition, Lock

import time

import datetime

from api.apiServer import start_api_server
from db.DataStore import store_data

from validator.Validator import validator, getMyIP
from spider.ProxyCrawl import startProxyCrawl

from config import TASK_QUEUE_SIZE, UPDATE_TIME

if __name__ == "__main__":
    myip = getMyIP()
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue(maxsize=TASK_QUEUE_SIZE)
    q2 = Queue()
    sleep_condition = Condition(Lock())
    p0 = Process(target=start_api_server, args=(sleep_condition, ))
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM, myip, sleep_condition))
    p2 = Process(target=validator, args=(q1, q2, myip))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM))
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print("sleep start:" + now)
        time.sleep(UPDATE_TIME)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print("sleep finish:" + now)
        sleep_condition.acquire()
        sleep_condition.notify()
        sleep_condition.release()

    p0.join()
    p1.join()
    p2.join()
    p3.join()
