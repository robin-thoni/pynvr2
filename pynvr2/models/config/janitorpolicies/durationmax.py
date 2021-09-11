import pydantic

from pynvr2.models.config.janitorpolicies.camerapolicybasemodel import CameraPolicyBaseModel


class DurationMaxConfigModel(CameraPolicyBaseModel):
    _NAME = 'camera_duration_max'

    name: str = pydantic.Field(default=_NAME, const=True)
    value: str = pydantic.Field()
