import pydantic

from pynvr2.models.config.janitorpolicies.policybasemodel import PolicyBaseModel


class DurationMaxConfigModel(PolicyBaseModel):
    name: str = pydantic.Field(default='duration_max', const=True)
    value: int = pydantic.Field()
