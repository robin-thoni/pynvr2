import pydantic

from pynvr2.models.args.argsbasemodel import ArgsBaseModel


class JanitorArgsModel(ArgsBaseModel):
    config_path: str = pydantic.Field(alias='config')
    dry: bool = pydantic.Field(default=False)
