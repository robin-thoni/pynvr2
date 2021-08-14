import pydantic

from pynvr2.models.args.argsbasemodel import ArgsBaseModel


class RecorderArgsModel(ArgsBaseModel):
    config_path: str = pydantic.Field(alias='config')
    camera: str = pydantic.Field()
