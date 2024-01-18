import secret_transfer.utils.cli.base as base


class LockboxPayload(base.CLICommand):
    _prefix = "yc lockbox payload"

    class KeyNotFoundError(base.CLICommand.BaseError):
        ...

    @classmethod
    def get(cls, profile_name: str, folder_name: str, lockbox_name: str, key: str) -> str:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        try:
            return cls._run(
                f"get"
                f" --profile {profile_name}"
                f" --folder-name {folder_name}"
                f" --name {lockbox_name}"
                f" --key {key}"
            )
        except base.RunError as exc:
            if exc.stderr.startswith("ERROR: payload entry with key"):
                raise cls.KeyNotFoundError(f"Key {key} is ot found in lockbox({lockbox_name})") from exc

            raise


class Lockbox(base.CLICommand):
    _prefix = "yc lockbox"

    payload = LockboxPayload


class YC(base.CLICommand):
    _prefix = "yc"

    lockbox = Lockbox
