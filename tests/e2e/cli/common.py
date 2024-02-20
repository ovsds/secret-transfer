import contextlib
import dataclasses
import subprocess
import typing


class SettingsFileContext(typing.Protocol):
    def __call__(self, content: str) -> contextlib.AbstractContextManager[str]: ...


@dataclasses.dataclass
class RunResult:
    stdout: str
    stderr: str
    exit_code: int


def run(command: str, encoding: str = "utf-8") -> RunResult:
    try:
        result = subprocess.run(command, check=True, capture_output=True, shell=True)
    except subprocess.CalledProcessError as exc:
        return RunResult(
            exit_code=exc.returncode,
            stdout=exc.stdout.decode(encoding),
            stderr=exc.stderr.decode(encoding),
        )

    return RunResult(
        exit_code=result.returncode,
        stdout=result.stdout.decode(encoding),
        stderr=result.stderr.decode(encoding),
    )
