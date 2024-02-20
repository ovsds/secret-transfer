import dataclasses
import subprocess


@dataclasses.dataclass
class RunError(Exception):
    exit_code: int
    stdout: str
    stderr: str
    command: str

    def __str__(self) -> str:
        return (
            f"Command '{self.command}' failed with exit code {self.exit_code}\n"
            f"STDOUT: {self.stdout}\n"
            f"STDERR: {self.stderr}"
        )


def run(command: str, encoding: str = "utf-8") -> str:
    try:
        result = subprocess.run(command, check=True, capture_output=True, shell=True)
    except subprocess.CalledProcessError as exc:
        raise RunError(
            exit_code=exc.returncode,
            stdout=exc.stdout.decode(encoding).strip("\n"),
            stderr=exc.stderr.decode(encoding).strip("\n"),
            command=command,
        ) from exc

    return result.stdout.decode(encoding)


class CLICommand:
    class BaseError(Exception): ...

    _prefix = ""

    @classmethod
    def _run(
        cls,
        command: str,
    ) -> str:
        return run(f"{cls._prefix} {command}")
