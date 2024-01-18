import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class BashExportDestination(core.AbstractDestination):
    def set(self, key: str, value: utils_types.BaseArgumentType) -> None:
        print(f"export {key}={value}")

    def clean(self, key: str) -> None:
        print(f"unset {key}")


def register_bash_nexport_destinatio_instance():
    BashExportDestination().register("bash_export")
