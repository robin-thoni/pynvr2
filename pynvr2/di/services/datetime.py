import abc
import datetime


class DateTime:
    @abc.abstractmethod
    def current(self) -> datetime.datetime:
        raise NotImplemented()
