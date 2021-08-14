import typing

import pydantic

from pynvr2.models.config.configbasemodel import ConfigBaseModel
from pynvr2.models.config.janitorpolicies.durationmax import DurationMaxConfigModel
from pynvr2.models.config.janitorpolicies.durationmin import DurationMinConfigModel


class CameraFfmpegInputModel(ConfigBaseModel):
    options: typing.Optional[str] = pydantic.Field()


class CameraFfmpegModel(ConfigBaseModel):
    input: CameraFfmpegInputModel = pydantic.Field(default=CameraFfmpegInputModel())


class CameraInputModel(ConfigBaseModel):
    url: str = pydantic.Field()
    # username: typing.Optional[str] = pydantic.Field()
    # password: typing.Optional[str] = pydantic.Field()


class CameraOutputModel(ConfigBaseModel):
    segment_time: str = pydantic.Field(default="10:00")
    pattern: str = pydantic.Field(default='%Y-%m-%d_%H-%M-%S.mp4')


class CameraJanitorPolicyModel(ConfigBaseModel):
    name: str = pydantic.Field()


class CameraJanitorModel(ConfigBaseModel):
    policies: typing.List[typing.Union[
        DurationMaxConfigModel,
        DurationMinConfigModel,
    ]] = pydantic.Field(default=[])


class CameraModel(ConfigBaseModel):
    name: str = pydantic.Field()
    ffmpeg: CameraFfmpegModel = pydantic.Field(default=CameraFfmpegModel())
    input: CameraInputModel = pydantic.Field()
    output: CameraOutputModel = pydantic.Field(default=CameraOutputModel())
    janitor: CameraJanitorModel = pydantic.Field(default=CameraJanitorModel())


class ConfigModel(ConfigBaseModel):
    cameras: typing.List[CameraModel] = pydantic.Field()
