import pydantic

import secret_transfer.core.transfer.base as base
import secret_transfer.protocol as protocol
import secret_transfer.utils.pydantic as pydantic_utils


class Arguments(pydantic_utils.BaseModel):
    collection: protocol.CollectionProtocol
    destination: protocol.DestinationProtocol

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class DefaultTransfer(base.AbstractTransfer):
    __default__ = True
    _arguments_model = Arguments

    def __init__(
        self,
        collection: protocol.CollectionProtocol,
        destination: protocol.DestinationProtocol,
    ):
        self._collection = collection
        self._destination = destination

    def run(self) -> None:
        collection = self._collection
        destination = self._destination

        try:
            items = collection.items()
        except protocol.CollectionProtocol.BaseError as exc:
            raise self.CollectionError("Collection failed") from exc

        for key, value in items:
            destination.set(key=key, value=value)

    def clean(self) -> None:
        collection = self._collection
        destination = self._destination

        for key in collection:
            destination.clean(key=key)
