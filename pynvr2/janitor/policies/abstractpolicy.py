import abc
import datetime
import typing

from pynvr2.janitor.policies.policyresult import PolicyResult


class AbstractPolicy(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        self._current_time: datetime.datetime = kwargs['current_time']

    @abc.abstractmethod
    def apply_policy(self, **kwargs) -> PolicyResult:
        raise NotImplemented()


class Policies:
    _types: typing.Dict[str, typing.Type] = {}
    _instances: typing.Dict[str, AbstractPolicy] = {}

    def register_policy(self, name: str, clazz: typing.Type):
        self._types[name] = clazz

    def instantiate_policies(self, **kwargs):
        for policy_type_name in self._types:
            self._instances[policy_type_name] = self._types[policy_type_name](**kwargs)

    def get_policy(self, name: str):
        return self._instances[name]


policies = Policies()


def register_policy(name: str):
    def register_policy_internal(clazz):
        policies.register_policy(name, clazz)
        return clazz
    return register_policy_internal
