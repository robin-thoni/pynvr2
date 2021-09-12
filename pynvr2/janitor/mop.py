import re
import typing

from pynvr2.janitor.mopdata import CameraData, RecordSegmentData
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.configmodel import ConfigModel
from pynvr2.di.services.io import IO
from pynvr2.di.services.recordsegmentdetails import RecordSegmentDetails
from pynvr2.janitor.policies.abstractpolicy import AbstractPolicy

import pynvr2.janitor.policies.policies  # Forces policies registrations


class Mop:
    def __init__(self, config: ConfigModel, io: IO, record_segment_details: RecordSegmentDetails, container):
        self.config = config
        self.io = io
        self.record_segment_details = record_segment_details
        self.container = container

    def get_cameras_data(self) -> typing.List[CameraData]:
        cameras_data = []
        for camera in self.config.cameras:
            camera_data = CameraData(camera)
            glob_pattern = re.sub('%.', '*', camera.output.pattern)
            files = sorted(self.io.glob(glob_pattern), key=lambda x:  self.record_segment_details.get_start_time(x, camera))
            camera_data.record_segments_data = [RecordSegmentData(f) for f in files]
            cameras_data.append(camera_data)
        return cameras_data

    def compute_policies(self, cameras_data: typing.List[CameraData]):
        for policy_config in self.config.janitor.policies:
            policy: AbstractPolicy = self.container.policies(policy_config.name)
            policy.apply_policy(policy_config, cameras_data)

    def apply_policies(self, cameras_data: typing.List[CameraData]):
        for camera_data in cameras_data:
            for record_segment_data in camera_data.record_segments_data:
                if record_segment_data.policy_result == PolicyResult.DELETE:
                    self.io.remove(record_segment_data.file_path)

    def sweep(self):
        cameras_data = self.get_cameras_data()
        self.compute_policies(cameras_data)
        self.apply_policies(cameras_data)
