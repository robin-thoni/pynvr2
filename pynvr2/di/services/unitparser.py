import abc


class UnitParser:
    @abc.abstractmethod
    def parse_timedelta(self, value: str):
        raise NotImplemented()

    @abc.abstractmethod
    def parse_bytes(self, value: str):
        raise NotImplemented()
