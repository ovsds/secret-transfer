import secret_transfer.core.transfer.base as base
import secret_transfer.protocol as protocol


class DefaultTransfer(base.AbstractTransfer):
    __default__ = True

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
            destination[key] = value

    def clean(self) -> None:
        collection = self._collection
        destination = self._destination

        for key in collection:
            del destination[key]
