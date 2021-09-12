import pydantic

from pynvr2.models.config.janitorpolicies.camerapolicybasemodel import CameraPolicyBaseModel


class DurationConfigModel(CameraPolicyBaseModel):
    value: str = pydantic.Field()


class DurationMinConfigModel(DurationConfigModel):
    _NAME = 'camera_duration_min'

    name: str = pydantic.Field(default=_NAME, const=True)


class DurationMaxConfigModel(DurationConfigModel):
    _NAME = 'camera_duration_max'

    name: str = pydantic.Field(default=_NAME, const=True)
