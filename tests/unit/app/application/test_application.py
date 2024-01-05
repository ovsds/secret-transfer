import pytest_mock

import secret_transfer.app as app
import secret_transfer.protocol as protocol


def test_from_settings():
    settings = app.ApplicationSettings()
    application = app.Application.from_settings(settings=settings)

    assert application.resources == app.ApplicationResources.from_registry()


def test_from_settings_exclude_registry(mocker: pytest_mock.MockerFixture):
    settings = app.ApplicationSettings()
    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    assert application.resources == app.ApplicationResources()


def test_from_settings_add_source_class(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        source_classes={
            "test_name": app.SourceClassSettings(
                module="test_module",
                class_name="test_class",
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_source_class.assert_called_once_with(
        name="test_name",
        settings=settings.source_classes["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_destination_class(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        destination_classes={
            "test_name": app.DestinationClassSettings(
                module="test_module",
                class_name="test_class",
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_destination_class.assert_called_once_with(
        name="test_name",
        settings=settings.destination_classes["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_collection_class(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        collection_classes={
            "test_name": app.CollectionClassSettings(
                module="test_module",
                class_name="test_class",
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_collection_class.assert_called_once_with(
        name="test_name",
        settings=settings.collection_classes["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_transfer_class(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        transfer_classes={
            "test_name": app.TransferClassSettings(
                module="test_module",
                class_name="test_class",
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_transfer_class.assert_called_once_with(
        name="test_name",
        settings=settings.transfer_classes["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_source(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        sources={
            "test_name": app.SourceSettings(
                class_name="test_class",
                init_args={"test_arg": "test_value"},
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_source.assert_called_once_with(
        name="test_name",
        settings=settings.sources["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_destination(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        destinations={
            "test_name": app.DestinationSettings(
                class_name="test_class",
                init_args={"test_arg": "test_value"},
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_destination.assert_called_once_with(
        name="test_name",
        settings=settings.destinations["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_collection(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        collections={
            "test_name": app.CollectionSettings(
                class_name="test_class",
                init_args={"test_arg": "test_value"},
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_collection.assert_called_once_with(
        name="test_name",
        settings=settings.collections["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_from_settings_add_transfer(mocker: pytest_mock.MockerFixture):
    patched_resources = mocker.patch("secret_transfer.app.application.ApplicationResources")
    settings = app.ApplicationSettings(
        transfers={
            "test_name": app.TransferSettings(
                class_name="test_class",
                init_args={"test_arg": "test_value"},
            ),
        },
    )

    application = app.Application.from_settings(settings=settings, exclude_registry=True)

    patched_resources.return_value.add_transfer.assert_called_once_with(
        name="test_name",
        settings=settings.transfers["test_name"],
    )
    assert application.resources == patched_resources.return_value


def test_run(mocker: pytest_mock.MockerFixture):
    mocked_resources = mocker.Mock(spec=app.ApplicationResources)
    mocked_resources.transfers = {"test_transfer_name": mocker.Mock(spec=protocol.TransferProtocol)}

    application = app.Application(resources=mocked_resources)

    application.run(transfer_name="test_transfer_name")

    mocked_resources.transfers["test_transfer_name"].run.assert_called_once_with()


def test_run_all(mocker: pytest_mock.MockerFixture):
    mocked_resources = mocker.Mock(spec=app.ApplicationResources)
    mocked_resources.transfers = {
        "test_transfer_name": mocker.Mock(spec=protocol.TransferProtocol),
        "test_transfer_name_2": mocker.Mock(spec=protocol.TransferProtocol),
    }

    application = app.Application(resources=mocked_resources)

    application.run_all()

    mocked_resources.transfers["test_transfer_name"].run.assert_called_once_with()
    mocked_resources.transfers["test_transfer_name_2"].run.assert_called_once_with()


def test_clean(mocker: pytest_mock.MockerFixture):
    mocked_resources = mocker.Mock(spec=app.ApplicationResources)
    mocked_resources.transfers = {"test_transfer_name": mocker.Mock(spec=protocol.TransferProtocol)}

    application = app.Application(resources=mocked_resources)

    application.clean(transfer_name="test_transfer_name")

    mocked_resources.transfers["test_transfer_name"].clean.assert_called_once_with()


def test_clean_all(mocker: pytest_mock.MockerFixture):
    mocked_resources = mocker.Mock(spec=app.ApplicationResources)
    mocked_resources.transfers = {
        "test_transfer_name": mocker.Mock(spec=protocol.TransferProtocol),
        "test_transfer_name_2": mocker.Mock(spec=protocol.TransferProtocol),
    }

    application = app.Application(resources=mocked_resources)

    application.clean_all()

    mocked_resources.transfers["test_transfer_name"].clean.assert_called_once_with()
    mocked_resources.transfers["test_transfer_name_2"].clean.assert_called_once_with()
