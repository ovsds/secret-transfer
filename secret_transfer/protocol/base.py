import typing

import typing_extensions


@typing.runtime_checkable
class BaseResourceProtocol(typing.Protocol):
    @classmethod
    def parse_init_arguments(cls, **arguments: typing.Any) -> typing.Mapping[str, typing.Any]:
        ...

    @classmethod
    def get_default_instances(cls) -> typing.Mapping[str, typing_extensions.Self]:
        ...


ResourceType = typing.TypeVar("ResourceType", bound=BaseResourceProtocol)
