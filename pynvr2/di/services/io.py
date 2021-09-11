import abc


class IO:
    @abc.abstractmethod
    def remove(self, path: str):
        raise NotImplemented()

    def size(self, path: str):
        raise NotImplemented()

    @abc.abstractmethod
    def glob(self, pattern: str):
        raise NotImplemented()
