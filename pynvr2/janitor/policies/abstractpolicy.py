import abc
import typing

from pynvr2.janitor.mopdata import CameraData
from pynvr2.models.config.janitorpolicies.policybasemodel import PolicyBaseModel


class AbstractPolicy(metaclass=abc.ABCMeta):
    def __init__(self, container):
        self.container = container

    @abc.abstractmethod
    def apply_policy(self, config: PolicyBaseModel, cameras_data: typing.List[CameraData]):
        raise NotImplemented()
