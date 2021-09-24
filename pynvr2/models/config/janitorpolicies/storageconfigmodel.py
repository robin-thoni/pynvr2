import pydantic

from pynvr2.models.config.janitorpolicies.camerapolicybasemodel import CameraPolicyBaseModel


class StorageMaxConfigModel(CameraPolicyBaseModel):
    _NAME = 'camera_storage_max'

    name: str = pydantic.Field(default=_NAME, const=True)
    size: str = pydantic.Field()
