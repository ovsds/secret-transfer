import contextlib
import contextvars
import os
import typing
import warnings

_root_path_context: contextvars.ContextVar[str] = contextvars.ContextVar("root_path")


@contextlib.contextmanager
def context_root_path(path: str) -> typing.Generator[str, None, None]:
    token = _root_path_context.set(path)
    try:
        yield path
    finally:
        _root_path_context.reset(token)


def set_root_path(path: str) -> None:
    _root_path_context.set(path)


def get_root_path() -> str:
    result = _root_path_context.get(None)

    if result is not None:
        return result

    warnings.warn(
        "Avoid using get_absolute_file_path with unset root_path context var, using CWD instead",
        category=RuntimeWarning,
    )

    return os.getcwd()


def get_absolute_file_path(file_path: str) -> str:
    if os.path.isabs(file_path):
        return file_path

    return os.path.join(get_root_path(), file_path)
