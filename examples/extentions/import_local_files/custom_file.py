import secret_transfer.core as secret_transfer_core
import secret_transfer.utils.types as secret_transfer_types


class CustomSource(secret_transfer_core.AbstractSource):
    def __getitem__(self, key: str) -> str:
        return "42"


class CustomDestination(secret_transfer_core.AbstractDestination):
    def set(self, key: str, value: secret_transfer_types.BaseArgumentType):
        print(f"CustomDestination.set called with key: {key} and value: {value}")

    def clean(self, key: str) -> None:
        print("CustomDestination.clean called with key: {key}")
