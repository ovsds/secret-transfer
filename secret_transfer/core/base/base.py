import abc
import typing

import typing_extensions

import secret_transfer.core.types as core_types
import secret_transfer.protocol as protocol


class BaseResource:
    ValidationError = protocol.BaseResourceProtocol.ValidationError

    @classmethod
    def parse_init_arguments(cls, **arguments: core_types.InitArgumentType) -> typing.Mapping[str, typing.Any]:
        return arguments

    @classmethod
    def get_default_instances(cls) -> typing.Mapping[str, typing_extensions.Self]:
        return {}

    @abc.abstractmethod
    def register(self, name: str) -> None: ...
