import typing

import secret_transfer.protocol as protocol


class RegistrationMeta(type):
    def __init__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, typing.Any]):
        cls.classes: dict[str, type] = {}
        cls.instances: dict[str, typing.Any] = {}
        cls.default_class: typing.Optional[type] = None


class BaseRegistry(type, typing.Generic[protocol.ResourceType], metaclass=RegistrationMeta):
    classes: dict[str, type[protocol.ResourceType]]
    instances: dict[str, protocol.ResourceType]
    default_class: typing.Optional[type[protocol.ResourceType]]

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, typing.Any],
    ):
        super().__init__(cls)

        if "__register__" not in attrs or attrs["__register__"]:
            cls.register_class(name, cls)  # pyright: ignore[reportGeneralTypeIssues]

        if "__default__" in attrs and attrs["__default__"]:
            cls.register_default_class(cls)  # pyright: ignore[reportGeneralTypeIssues]

    @classmethod
    def register_class(cls, name: str, class_: type[protocol.ResourceType]) -> None:
        if name in cls.classes:
            raise ValueError(f"Duplicate class {name}")

        cls.classes[name] = class_

    @classmethod
    def register_default_class(cls, class_: type[protocol.ResourceType], force: bool = False) -> None:
        if cls.default_class is not None and not force:  # pyright: ignore[reportUnnecessaryComparison]
            raise ValueError("Default instance already registered")

        cls.default_class = class_

    @classmethod
    def register_instance(cls, name: str, instance: protocol.ResourceType) -> None:
        if name in cls.instances:
            raise ValueError(f"Duplicate instance {name}")

        cls.instances[name] = instance
