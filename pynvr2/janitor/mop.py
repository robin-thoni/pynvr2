import glob
import os
import re
import typing
import datetime

from pynvr2.janitor.mopdata import CameraData, RecordSegmentData
from pynvr2.janitor.policies.abstractpolicy import PolicyResult, policies
from pynvr2.models.args.janitorargsmodel import JanitorArgsModel
from pynvr2.models.config.configmodel import ConfigModel
from pynvr2.models.recordsegmentmodel import RecordSegmentModel

import pynvr2.janitor.policies.policies  # Forces policies registrations


class Mop:
    def __init__(self, options: JanitorArgsModel, config: ConfigModel):
        self.options = options
        self.config = config

    def get_cameras_data(self) -> typing.List[CameraData]:
        cameras_data = []
        for camera in self.config.cameras:
            camera_data = CameraData(camera)
            glob_pattern = re.sub('%.', '*', camera.output.pattern)
            files = glob.glob(glob_pattern)
            for file_path in files:
                file_date = datetime.datetime.strptime(file_path, camera.output.pattern)
                duration = datetime.timedelta(hours=0)  # TODO compute `duration`
                camera_data.record_segments_data.append(RecordSegmentData(RecordSegmentModel(file_date, duration), file_path))
            camera_data.record_segments_data.sort(key=lambda x: x.record_segment.start_date)
            cameras_data.append(camera_data)
        return cameras_data

    def compute_policies(self, cameras_data: typing.List[CameraData]):
        for camera_data in cameras_data:
            for record_segment_data in camera_data.record_segments_data:
                for policy in camera_data.camera.janitor.policies:
                    policy_instance = policies.get_policy(policy.name)
                    policy_result = policy_instance.apply_policy(
                        options=self.options,
                        config=self.config,
                        cameras_data=cameras_data,
                        camera_data=camera_data,
                        record_segment_data=record_segment_data,
                        policy=policy,
                    )
                    if policy_result in [PolicyResult.PRESERVE, PolicyResult.DELETE]:
                        record_segment_data.policy_result = policy_result
                    print('{}: {} - {} = {}'.format(camera_data.camera.name, record_segment_data.record_segment.start_date, policy.name, policy_result))

    def apply_policies(self, cameras_data: typing.List[CameraData]):
        for camera_data in cameras_data:
            for record_segment_data in camera_data.record_segments_data:
                if record_segment_data.policy_result == PolicyResult.DELETE:
                    if not self.options.dry:
                        os.remove(record_segment_data.file_path)
                    print('{}DELETING {}'.format('[DRY RUN] ' if self.options.dry else '', record_segment_data.file_path))

    def sweep(self):
        policies.instantiate_policies(
            current_time=datetime.datetime.now(),
        )

        cameras_data = self.get_cameras_data()
        self.compute_policies(cameras_data)
        self.apply_policies(cameras_data)
