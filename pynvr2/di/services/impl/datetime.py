from pynvr2.di.services.datetime import DateTime


class DateTimeImpl(DateTime):
    def __init__(self, value):
        self.value = value

    def current(self):
        return self.value
