import dataclasses
import importlib
import typing

import lazy_object_proxy

import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types


@dataclasses.dataclass
class ResourceClassSettings(typing.Generic[protocol.ResourceType]):
    module: str
    class_name: str


@dataclasses.dataclass
class ResourceSettings(typing.Generic[protocol.ResourceType]):
    resource_classes: typing.Mapping[str, type[protocol.ResourceType]]
    default_resource_class: typing.Optional[type[protocol.ResourceType]] = None
    resources: typing.Mapping[str, typing.Mapping[str, protocol.BaseResourceProtocol]] = dataclasses.field(
        default_factory=dict
    )

    class_name: typing.Optional[str] = None
    raw_arguments: typing.Mapping[str, typing.Any] = dataclasses.field(default_factory=dict)


class BaseClassProxy(typing.Generic[protocol.ResourceType]):
    _proxy_protocol = NotImplemented

    class BaseError(Exception):
        ...

    class ImportError(BaseError):
        ...

    class InvalidProtocolError(BaseError):
        ...

    @classmethod
    def from_settings(cls, settings: ResourceClassSettings[protocol.ResourceType]) -> type[protocol.ResourceType]:
        def factory() -> type[protocol.ResourceType]:
            return cls._get_target(settings=settings)

        return typing.cast(type[protocol.ResourceType], lazy_object_proxy.Proxy(factory))

    @classmethod
    def _get_target(cls, settings: ResourceClassSettings[protocol.ResourceType]) -> type[protocol.ResourceType]:
        try:
            module = importlib.import_module(settings.module)
        except ModuleNotFoundError as exc:
            raise cls.ImportError(f"Module({settings.module}) is not found") from exc

        try:
            source_class = getattr(module, settings.class_name)
        except AttributeError as exc:
            raise cls.ImportError(f"Class({settings.class_name}) is not found in module({settings.module})") from exc

        if not issubclass(source_class, cls._proxy_protocol):
            raise cls.InvalidProtocolError(
                f"Class({source_class.__name__}) does not implement the protocol({cls._proxy_protocol.__name__})"
            )
        return source_class


@typing.runtime_checkable
class GettableResourceProtocol(typing.Protocol):
    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        ...


InitArgumentsType = typing.Union[
    utils_types.LiteralArgumentType,
    protocol.BaseResourceProtocol,
    dict[str, "InitArgumentsType"],
    list["InitArgumentsType"],
]


@dataclasses.dataclass
class ResourceArgument:
    type: str
    name: str
    key: typing.Optional[str] = None


class ParseResourceArgumentError(Exception):
    ...


def _get_bracket_block(value: str) -> str:
    assert value.startswith("["), "Resource argument bracket block must start with '['"

    bracket_count = 0
    for index, char in enumerate(value):
        if char == "[":
            bracket_count += 1
        elif char == "]":
            bracket_count -= 1

        if bracket_count == 0:
            return value[: index + 1]

    raise ValueError(f"bracket block must end with ']', got {value!r}")


def _parse_resource_argument(argument: str) -> ResourceArgument:
    # TODO: refactor using regex
    error_message = """
    Invalid resource argument({argument!r}) format: {description}
    Expected format:
    $<resource_type>[<resource_name>] for resource
    $<resource_type>[<resource_name>][<key>] for resource value
    Nested argument is supported
    """

    assert argument.startswith("$"), "Resource argument must start with $"

    try:
        block_start_index = argument.index("[")
    except ValueError as exc:
        raise ParseResourceArgumentError(
            error_message.format(argument=argument, description="must contain at least one block")
        ) from exc

    resource_type = argument[1:block_start_index]
    rest = argument[block_start_index:]
    try:
        next_block = _get_bracket_block(rest)
    except ValueError as exc:
        raise ParseResourceArgumentError(error_message.format(argument=argument, description=str(exc))) from exc
    resource_name = next_block[1:-1]

    rest = rest[len(next_block) :]
    if rest == "":
        return ResourceArgument(type=resource_type, name=resource_name)

    try:
        next_block = _get_bracket_block(rest)
    except ValueError as exc:
        raise ParseResourceArgumentError(error_message.format(argument=argument, description=str(exc))) from exc
    key = next_block[1:-1]

    rest = rest[len(next_block) :]
    if rest != "":
        raise ParseResourceArgumentError(
            error_message.format(
                argument=argument, description="must have at most 2 blocks, first for resource name, second for key"
            )
        )

    return ResourceArgument(type=resource_type, name=resource_name, key=key)


class BaseResourceProxy(typing.Generic[protocol.ResourceType]):
    class BaseError(Exception):
        ...

    class ClassNotFoundError(BaseError):
        ...

    class InvalidResourceArgumentFormatError(BaseError):
        ...

    class ResourceTypeNotFoundError(BaseError):
        ...

    class ResourceNotFoundError(BaseError):
        ...

    class InvalidResourceTypeError(BaseError):
        ...

    class ResourceError(BaseError):
        ...

    class ParseArgumentsError(BaseError):
        ...

    @classmethod
    def from_settings(cls, settings: ResourceSettings[protocol.ResourceType]) -> protocol.ResourceType:
        def factory() -> protocol.ResourceType:
            return cls._get_target(settings=settings)

        return typing.cast(protocol.ResourceType, lazy_object_proxy.Proxy(factory))

    @classmethod
    def _get_target(cls, settings: ResourceSettings[protocol.ResourceType]) -> protocol.ResourceType:
        resource_class = cls._get_class(settings=settings)
        arguments = cls._get_arguments(settings=settings)
        parsed_arguments = resource_class.parse_init_arguments(**arguments)

        return resource_class(**parsed_arguments)

    @classmethod
    def _get_class(cls, settings: ResourceSettings[protocol.ResourceType]) -> type[protocol.ResourceType]:
        if settings.class_name is None:
            if settings.default_resource_class is None:
                raise cls.ClassNotFoundError("Either class_name or default_collection_class must be set")

            return settings.default_resource_class

        try:
            return settings.resource_classes[settings.class_name]
        except KeyError as exc:
            raise cls.ClassNotFoundError(f"Unknown class {settings.class_name!r}") from exc

    @classmethod
    def _get_resource_argument_value(
        cls,
        settings: ResourceSettings[protocol.ResourceType],
        raw_argument: str,
    ) -> typing.Union[protocol.BaseResourceProtocol, utils_types.LiteralArgumentType]:
        try:
            argument = _parse_resource_argument(argument=raw_argument)
        except ParseResourceArgumentError as exc:
            raise cls.InvalidResourceArgumentFormatError(str(exc)) from exc

        try:
            resources = settings.resources[argument.type]
        except KeyError as exc:
            raise cls.ResourceTypeNotFoundError(f"Unknown resource type({argument.type!r})") from exc

        resource_name = cls._get_literal_argument_value(settings=settings, raw_argument=argument.name)

        if not isinstance(resource_name, str):
            raise cls.InvalidResourceArgumentFormatError(
                f"Resource name({resource_name!r}) must be string literal or resolvable to string literal"
            )

        try:
            resource = resources[resource_name]
        except KeyError as exc:
            raise cls.ResourceNotFoundError(f"Unknown resource({resource_name!r})") from exc

        if argument.key is None:
            return resource

        key = cls._get_literal_argument_value(settings=settings, raw_argument=argument.key)
        if not isinstance(key, str):
            raise cls.InvalidResourceArgumentFormatError(
                f"Key({key!r}) must be string literal or resolvable to string literal"
            )

        if not isinstance(resource, GettableResourceProtocol):
            raise cls.InvalidResourceTypeError(
                f"Resource({resource_name!r}) does not implement [__getitem__(str) -> str | int | float | bool] method"
            )

        def factory() -> utils_types.LiteralArgumentType:
            try:
                return resource[key]
            except Exception as exc:
                raise cls.ResourceError(f"Key({key!r}) is not found in resource({resource_name!r})") from exc

        return typing.cast(utils_types.LiteralArgumentType, lazy_object_proxy.Proxy(factory))

    @classmethod
    def _get_literal_argument_value(
        cls,
        settings: ResourceSettings[protocol.ResourceType],
        raw_argument: utils_types.LiteralArgumentType,
    ) -> InitArgumentsType:
        if isinstance(raw_argument, str) and raw_argument.startswith("$"):
            return cls._get_resource_argument_value(settings=settings, raw_argument=raw_argument)

        return raw_argument

    @classmethod
    def _get_argument_value(
        cls,
        settings: ResourceSettings[protocol.ResourceType],
        raw_argument: utils_types.BaseArgumentType,
    ) -> InitArgumentsType:
        if isinstance(raw_argument, dict):
            return {
                key: cls._get_argument_value(settings=settings, raw_argument=value)
                for key, value in raw_argument.items()
            }

        if isinstance(raw_argument, list):
            return [cls._get_argument_value(settings=settings, raw_argument=value) for value in raw_argument]

        return cls._get_literal_argument_value(settings=settings, raw_argument=raw_argument)

    @classmethod
    def _get_arguments(
        cls, settings: ResourceSettings[protocol.ResourceType]
    ) -> typing.Mapping[str, InitArgumentsType]:
        return {
            key: cls._get_argument_value(settings=settings, raw_argument=value)
            for key, value in settings.raw_arguments.items()
        }
