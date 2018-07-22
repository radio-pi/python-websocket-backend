from time import time
from threading import Timer


class Sleep():
    def __init__(self, sleepInMinutes, callbackFnc):
        self.__time_in_sec = sleepInMinutes * 60
        self.__callback = callbackFnc
        self.__start_time = time()
        self.start()

    def start(self):
        print("start sleep timer with " + str(self.__time_in_sec))
        self.__timer = Timer(self.__time_in_sec, self.__callback)
        self.__timer.start()

    def cancel(self):
         self.__timer.cancel()

    def remaining(self):
        # time passed - time set * 60 for minutes
        print(time())
        print(self.__start_time)
        remaining_time = (self.__time_in_sec - (time() - self.__start_time)) / 60

        if remaining_time < 0:
            remaining_time = 0
        
        return int(remaining_time)
