import secret_transfer.utils.cli.base as base


class Repo(base.CLICommand):
    _prefix = "gh repo"

    @classmethod
    def view(cls, json: str, template: str) -> str:
        return cls._run(f"view --json {json} --template {template}")

    @classmethod
    def get_name(cls) -> str:
        return cls.view(json="name", template="{{.name}}")

    @classmethod
    def get_owner_name(cls) -> str:
        return cls.view(json="owner", template="{{.owner.login}}")


class Secret(base.CLICommand):
    _prefix = "gh secret"

    class KeyNotFoundError(base.CLICommand.BaseError):
        ...

    @classmethod
    def set(cls, key: str, value: str, repo_url: str) -> None:
        cls._run(f'set {key} --body "{value}" --repo {repo_url}')

    @classmethod
    def delete(cls, key: str, repo_url: str) -> None:
        try:
            cls._run(f"delete {key} --repo {repo_url}")
        except base.RunError as exc:
            if exc.stderr.startswith("failed to delete secret test_key: HTTP 404"):
                raise cls.KeyNotFoundError(f"Key({key}) not found") from exc

            raise


class GH(base.CLICommand):
    _prefix = "gh"

    repo = Repo
    secret = Secret
