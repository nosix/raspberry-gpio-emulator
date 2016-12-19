import time
from threading import Timer


class SyncTask:
    def __init__(self, task):
        self.__waiting = True
        self.__task = task

    def start(self, timeout=None):
        # type: (int) -> None
        if timeout is not None:
            Timer(timeout / 1000, self.__callback).start()

    def __callback(self):
        # type: () -> None
        self.__waiting = False

    def alive(self):
        # type: () -> bool
        time.sleep(0.1)
        return self.__waiting

    def do_task(self):
        return self.__task()
