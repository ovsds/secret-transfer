import dataclasses
import typing

import pydantic

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import secret_transfer.utils.pydantic as pydantic_utils
import secret_transfer.utils.types as utils_types


@dataclasses.dataclass
class DefaultCollectionItem:
    source: protocol.SourceProtocol
    key: typing.Optional[str] = None


class Arguments(pydantic_utils.BaseModel):
    items: typing.Mapping[str, DefaultCollectionItem]

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class DefaultCollection(core.AbstractCollection):
    __default__ = True

    def __init__(self, **items: DefaultCollectionItem):
        self._items = items

    @classmethod
    def parse_init_arguments(cls, **arguments: utils_types.BaseArgumentType) -> typing.Mapping[str, typing.Any]:
        model = Arguments.model_validate({"items": arguments})
        return model.items

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
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

    def items(self) -> typing.Iterator[tuple[str, utils_types.LiteralArgumentType]]:
        for key in self:
            yield key, self[key]
