import os.path
import typing

import click
import pydantic

import secret_transfer.app as app
import secret_transfer.context as context
import secret_transfer.utils.pydantic as pydantic_utils


def read_settings(file_path: str) -> app.ApplicationSettings:
    try:
        with open(file_path, encoding="utf-8") as file:
            raw = file.read()
    except FileNotFoundError:
        raise click.FileError(filename=file_path, hint="File not found")

    try:
        return app.ApplicationSettings.from_yaml(raw=raw)
    except pydantic_utils.PydanticYamlLoadError as exc:
        raise click.UsageError(message=f"Failed to load settings file from {file_path}: \n{exc.message}")
    except pydantic.ValidationError as exc:
        message = pydantic_utils.format_validation_error(exception=exc)
        raise click.UsageError(message=f"Failed to validate settings schema for {file_path}: \n{message}")


def get_application(file_path: str) -> app.Application:
    settings = read_settings(file_path=file_path)

    context.set_root_path(os.path.dirname(file_path))

    return app.Application.from_settings(settings=settings)


@click.group()
def main():
    pass


@main.command(
    name="run",
    help="Run transfers.",
)
@click.option(
    "-f",
    "--file_path",
    help="Path to the application settings file.",
    type=str,
    required=True,
)
@click.option(
    "-n",
    "--name",
    help="Name of the transfer to run, if not specified, all transfers will be run.",
    type=str,
    default=None,
)
def run(file_path: str, name: typing.Optional[str] = None):
    application = get_application(file_path=file_path)

    if name is not None:
        return application.run(transfer_name=name)

    return application.run_all()


@main.command(
    name="clean",
    help="Clean up the transfer's destinations.",
)
@click.option(
    "-f",
    "--file_path",
    help="Path to the application settings file.",
    type=str,
    required=True,
)
@click.option(
    "-n",
    "--name",
    help="Name of the transfer, if not specified, all transfers will be cleaned.",
    type=str,
    default=None,
)
def clean(file_path: str, name: typing.Optional[str] = None):
    application = get_application(file_path=file_path)

    if name is not None:
        return application.clean(transfer_name=name)

    return application.clean_all()


__all__ = [
    "main",
]
