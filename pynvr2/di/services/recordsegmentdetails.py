import abc
import typing
from datetime import datetime, timedelta

from pynvr2.models.config.configmodel import CameraModel


class RecordSegmentDetails:
    @abc.abstractmethod
    def get_start_time(self, path: str, camera: CameraModel) -> datetime:
        raise NotImplemented()

    @abc.abstractmethod
    def get_duration(self, path: str, camera: CameraModel) -> typing.Optional[timedelta]:
        raise NotImplemented()

    @abc.abstractmethod
    def get_end_time(self, path: str, camera: CameraModel) -> typing.Optional[datetime]:
        raise NotImplemented()
