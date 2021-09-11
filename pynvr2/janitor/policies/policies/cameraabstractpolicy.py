import fnmatch
import re

from pynvr2.janitor.policies.abstractpolicy import AbstractPolicy
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
