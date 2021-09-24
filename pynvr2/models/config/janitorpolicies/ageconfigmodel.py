import pydantic

from pynvr2.models.config.janitorpolicies.camerapolicybasemodel import CameraPolicyBaseModel


class AgeConfigModel(CameraPolicyBaseModel):
    age: str = pydantic.Field()


class AgeMinConfigModel(AgeConfigModel):
    _NAME = 'segment_age_min'

    name: str = pydantic.Field(default=_NAME, const=True)


class AgeMaxConfigModel(AgeConfigModel):
    _NAME = 'segment_age_max'

    name: str = pydantic.Field(default=_NAME, const=True)
