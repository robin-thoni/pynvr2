import typing


class PoliciesStore:
    _types: typing.Dict[str, typing.Type] = {}

    def register(self, name: str):
        def register_policy_internal(clazz):
            self._types[name] = clazz
            return clazz
        return register_policy_internal

    def instanciate(self, container, name: str):
        return self._types[name](container)


policies = PoliciesStore()
