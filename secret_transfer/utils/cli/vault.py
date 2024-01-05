import secret_transfer.utils.cli.base as base


class KV(base.CLICommand):
    _prefix = "vault kv"

    class MountForbiddenError(base.CLICommand.BaseError):
        ...

    class SecretNotFoundError(base.CLICommand.BaseError):
        ...

    class KeyNotFoundError(base.CLICommand.BaseError):
        ...

    @classmethod
    def get(cls, address: str, mount: str, field: str, value: str) -> str:
        """
        :raises MountForbiddenError: if access to mount is forbidden
        :raises SecretNotFoundError: if the secret is not found
        :raises KeyNotFoundError: if the key is not found
        """
        try:
            return cls._run(f"get" f" -address={address}" f" -mount={mount}" f" -field={field}" f" {value}")
        except base.RunError as exc:
            if "Code: 403" in exc.stderr:
                raise cls.MountForbiddenError(f"Access to mount({mount}) is forbidden") from exc
            if exc.stderr.startswith("No value found at "):
                raise cls.SecretNotFoundError(f"Secret({value}) not found") from exc
            if exc.stderr.startswith(f'Field "{field}" not present in secret'):
                raise cls.KeyNotFoundError(f"Key({field}) not found") from exc

            raise


class Vault(base.CLICommand):
    _prefix = "vault"

    kv = KV
