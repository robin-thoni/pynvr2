import abc
import fnmatch
import re
import typing

from pynvr2.janitor.mopdata import CameraData, RecordSegmentData
from pynvr2.janitor.policies.abstractpolicy import AbstractPolicy
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.configmodel import CameraModel
from pynvr2.models.config.janitorpolicies.camerapolicybasemodel import CameraPolicyBaseModel, CameraFilterItem, \
    CameraFilterItemType


class CameraAbstractPolicy(AbstractPolicy):
    def _match_str(self, filter_item: CameraFilterItem, data: str) -> bool:
        if filter_item.type == CameraFilterItemType.GLOB:
            return fnmatch.fnmatch(data, filter_item.filter)
        elif filter_item.type == CameraFilterItemType.REGEX:
            m = re.search(filter_item.filter, data)
            return True if m else False
        return False

    def _match_camera(self, config: CameraPolicyBaseModel, camera: CameraModel) -> bool:
        for item in config.cameras:
            if self._match_str(item, camera.name):
                return True
        return False

    @abc.abstractmethod
    def get_record_segment_policy(self, config: CameraPolicyBaseModel, camera_data: CameraData, record_segment_data: RecordSegmentData) -> PolicyResult:
        raise NotImplemented()

    def apply_policy(self, config: CameraPolicyBaseModel, cameras_data: typing.List[CameraData]):
        for camera_data in cameras_data:
            if self._match_camera(config, camera_data.camera):
                for record_segment_data in camera_data.record_segments_data:
                    policy_result = self.get_record_segment_policy(config, camera_data, record_segment_data)
                    if policy_result in [PolicyResult.DELETE, PolicyResult.PRESERVE]:
                        record_segment_data.policy_result = policy_result
