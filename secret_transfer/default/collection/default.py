import dataclasses
import typing

import typing_extensions

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types


@dataclasses.dataclass
class DefaultCollectionItem:
    source: protocol.SourceProtocol
    key: typing.Optional[str] = None

    @classmethod
    def from_init_arguments(cls, data: core.InitArgumentType) -> typing_extensions.Self:
        if not isinstance(data, typing.Mapping):
            raise ValueError("Should be a mapping.")

        source = data.get("source")
        if source is None:
            raise ValueError("Should have a source.")
        if not isinstance(source, protocol.SourceProtocol):
            raise ValueError("Should have a source of type SourceProtocol.")

        key = data.get("key")
        if key is not None and not isinstance(key, str):
            raise ValueError("Should have a key of type str or None.")

        return cls(source=source, key=key)


class DefaultCollection(core.AbstractCollection):
    __default__ = True

    def __init__(self, **items: DefaultCollectionItem):
        self._items = items

    @classmethod
    def parse_init_arguments(cls, **items: core.InitArgumentType) -> typing.Mapping[str, DefaultCollectionItem]:
        result: dict[str, DefaultCollectionItem] = {}

        for key, value in items.items():
            try:
                result[key] = DefaultCollectionItem.from_init_arguments(value)
            except ValueError as exc:
                raise cls.ValidationError(f"Error parsing item {key}: {exc}") from exc

        return result

    def __getitem__(self, key: str) -> utils_types.Literal:
        try:
            item = self._items[key]
        except KeyError as exc:
            raise self.KeyNotFoundError(f"Key {key} is not found in collection {self.__class__.__name__}") from exc

        try:
            key = item.key or key
            return item.source[key]
        except protocol.SourceProtocol.KeyNotFoundError as exc:
            raise self.KeyNotFoundError(f"Key {key} is not found in source {item.source}") from exc

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self._items)

    def items(self) -> typing.Iterator[tuple[str, utils_types.Literal]]:
        for key in self:
            yield key, self[key]
