import typing

from pynvr2.janitor.mopdata import CameraData
from pynvr2.janitor.policies.policies.cameraabstractpolicy import CameraAbstractPolicy
from pynvr2.janitor.policies.policiesstore import policies
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.janitorpolicies.durationmin import DurationMinConfigModel


@policies.register(DurationMinConfigModel._NAME)
class DurationMinPolicy(CameraAbstractPolicy):

    def apply_policy(self, config: DurationMinConfigModel, cameras_data: typing.List[CameraData]):
        for camera_data in cameras_data:
            if self._match_camera(config, camera_data.camera):
                for record_segment_data in camera_data.record_segments_data:
                    current_time = self.container.datetime().current()
                    start_time = self.container.record_segment_details().get_start_time(record_segment_data.file_path, camera_data.camera)
                    diff = current_time - start_time
                    config_value = self.container.unit_parser().parse_timedelta(config.value)
                    if diff <= config_value:
                        record_segment_data.policy_result = PolicyResult.PRESERVE
