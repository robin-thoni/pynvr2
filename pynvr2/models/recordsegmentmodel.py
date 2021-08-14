import datetime
import typing


class RecordSegmentModel:
    def __init__(self, start_date: datetime.datetime, duration: datetime.timedelta):
        self.start_date = start_date
        self.duration: typing.Optional[datetime.timedelta] = duration

    @property
    def end_date(self) -> typing.Optional[datetime.datetime]:
        if self.duration:
            return self.start_date + self.duration
        else:
            return None
