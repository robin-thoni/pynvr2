import typing

from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.configmodel import CameraModel


class RecordSegmentData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.policy_result: PolicyResult = PolicyResult.IGNORE


class CameraData:
    def __init__(self, camera: CameraModel):
        self.camera = camera
        self.record_segments_data: typing.List[RecordSegmentData] = []
