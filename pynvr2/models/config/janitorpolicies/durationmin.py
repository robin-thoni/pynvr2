import pydantic

from pynvr2.models.config.janitorpolicies.policybasemodel import PolicyBaseModel


class DurationMinConfigModel(PolicyBaseModel):
    name: str = pydantic.Field(default='duration_min', const=True)
    value: int = pydantic.Field()
