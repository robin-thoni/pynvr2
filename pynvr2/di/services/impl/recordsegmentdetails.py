import re
import subprocess
import typing

from pynvr2.di.services.recordsegmentdetails import RecordSegmentDetails
from datetime import datetime, timedelta

from pynvr2.models.config.configmodel import CameraModel


class RecordSegmentDetailsImpl(RecordSegmentDetails):
    def get_start_time(self, path: str, camera: CameraModel) -> datetime:
        return datetime.strptime(path, camera.output.pattern)

    def get_duration(self, path: str, camera: CameraModel) -> timedelta:
        r = subprocess.run(['ffmpeg', '-i', path], stderr=subprocess.PIPE)
        m = re.match('Duration: (\\d+):(\\d+):(\\d+)\\.(\\d+)', r.stderr.decode('UTF-8'))
        if m:
            return timedelta(hours=int(m.group(1)), minutes=int(m.group(2)), seconds=int(m.group(3)), milliseconds=int(m.group(4)))
        raise ValueError()

    def get_end_time(self, path: str, camera: CameraModel) -> typing.Optional[datetime]:
        duration = self.get_duration(path, camera)
        if duration is None:
            return None
        return self.get_start_time(path, camera) + duration
