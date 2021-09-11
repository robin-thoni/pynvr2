import typing
from enum import Enum

import pydantic

from pynvr2.models.config.janitorpolicies.policybasemodel import PolicyBaseModel


class CameraFilterItemType(Enum):
    GLOB = 'glob'
    REGEX = 'regex'


class CameraFilterItem(PolicyBaseModel):
    filter: str = pydantic.Field()
    type: CameraFilterItemType = pydantic.Field(default=CameraFilterItemType.GLOB)


class CameraPolicyBaseModel(PolicyBaseModel):
    cameras: typing.List[CameraFilterItem] = pydantic.Field(default=[CameraFilterItem(filter='*')])

    @pydantic.validator('cameras', pre=True, allow_reuse=True)
    def map_cameras(cls, v):
        for i in range(len(v)):
            if isinstance(v[i], str):
                v[i] = {
                    'filter': v[i]
                }
        return v
