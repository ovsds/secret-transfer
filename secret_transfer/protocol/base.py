import typing


@typing.runtime_checkable
class BaseResourceProtocol(typing.Protocol):
    @classmethod
    def parse_init_arguments(cls, **arguments: typing.Any) -> typing.Mapping[str, typing.Any]:
        ...


ResourceType = typing.TypeVar("ResourceType", bound=BaseResourceProtocol)
