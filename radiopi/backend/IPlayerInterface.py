from abc import ABCMeta, abstractmethod


class IPlayer:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def play(self, url): raise NotImplementedError

    @abstractmethod
    def stop(self): raise NotImplementedError

    @abstractmethod
    def get_volume(self): raise NotImplementedError

    @abstractmethod
    def get_title(self): raise NotImplementedError

    @abstractmethod
    def set_volume(self, volume): raise NotImplementedError

    @abstractmethod
    def get_sleep_timer(self): raise NotImplementedError

    @abstractmethod
    def set_sleep_timer(self, timeInMinutes): raise NotImplementedError
