import abc
import datetime

from pynvr2.janitor.mopdata import CameraData, RecordSegmentData
from pynvr2.janitor.policies.policies.cameraabstractpolicy import CameraAbstractPolicy
from pynvr2.janitor.policies.policiesstore import policies
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.janitorpolicies.ageconfigmodel import AgeMaxConfigModel, AgeMinConfigModel


class AgePolicy(CameraAbstractPolicy):
    @abc.abstractmethod
    def _get_policy(self, diff: datetime.timedelta, config_value: datetime.timedelta) -> PolicyResult:
        raise NotImplemented()

    def get_record_segment_policy(self, config: AgeMaxConfigModel, camera_data: CameraData,
                                  record_segment_data: RecordSegmentData) -> PolicyResult:
        current_time = self.container.datetime().current()
        start_time = self.container.record_segment_details().get_start_time(record_segment_data.file_path, camera_data.camera)
        diff = current_time - start_time
        config_value = self.container.unit_parser().parse_timedelta(config.age)
        return self._get_policy(diff, config_value)


@policies.register(AgeMaxConfigModel._NAME)
class AgeMaxPolicy(AgePolicy):
    def _get_policy(self, diff: datetime.timedelta, config_value: datetime.timedelta) -> PolicyResult:
        if diff >= config_value:
            return PolicyResult.DELETE
        return PolicyResult.IGNORE


@policies.register(AgeMinConfigModel._NAME)
class AgeMinPolicy(AgePolicy):
    def _get_policy(self, diff: datetime.timedelta, config_value: datetime.timedelta) -> PolicyResult:
        if diff <= config_value:
            return PolicyResult.PRESERVE
        return PolicyResult.IGNORE
