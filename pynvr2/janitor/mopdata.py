import typing

from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.configmodel import CameraModel
from pynvr2.models.recordsegmentmodel import RecordSegmentModel


class RecordSegmentData:
    def __init__(self, record_segment: RecordSegmentModel, file_path: str):
        self.record_segment = record_segment
        self.file_path = file_path
        self.policy_result: PolicyResult = PolicyResult.IGNORE


class CameraData:
    def __init__(self, camera: CameraModel):
        self.camera = camera
        self.record_segments_data: typing.List[RecordSegmentData] = []

