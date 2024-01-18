import pytest_mock

import secret_transfer.app as app
import secret_transfer.core as core


def test_from_registry_source_classes():
    resources = app.ApplicationResources.from_registry()

    assert resources.source_classes == core.SourceRegistry.classes
    assert resources.destination_classes == core.DestinationRegistry.classes
    assert resources.collection_classes == core.CollectionRegistry.classes
    assert resources.transfer_classes == core.TransferRegistry.classes

    assert resources.default_source_class == core.SourceRegistry.default_class
    assert resources.default_destination_class == core.DestinationRegistry.default_class
    assert resources.default_collection_class == core.CollectionRegistry.default_class
    assert resources.default_transfer_class == core.TransferRegistry.default_class

    assert resources.sources == core.SourceRegistry.instances
    assert resources.destinations == core.DestinationRegistry.instances
    assert resources.collections == core.CollectionRegistry.instances
    assert resources.transfers == core.TransferRegistry.instances


def test_add_source_class(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.SourceClassProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.source_classes == {}

    resources.add_source_class(
        name="test_name",
        settings=app.SourceClassSettings(
            module="test_module",
            class_name="test_class",
        ),
    )

    assert resources.source_classes == {"test_name": patched_proxy.return_value}
    patched_proxy.assert_called_once_with(
        settings=core.SourceClassSettings(
            module="test_module",
            class_name="test_class",
        )
    )


def test_add_destination_class(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.DestinationClassProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.destination_classes == {}

    resources.add_destination_class(
        name="test_name",
        settings=app.DestinationClassSettings(
            module="test_module",
            class_name="test_class",
        ),
    )

    assert resources.destination_classes == {"test_name": patched_proxy.return_value}
    patched_proxy.assert_called_once_with(
        settings=core.DestinationClassSettings(
            module="test_module",
            class_name="test_class",
        )
    )


def test_add_collection_class(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.CollectionClassProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.collection_classes == {}

    resources.add_collection_class(
        name="test_name",
        settings=app.CollectionClassSettings(
            module="test_module",
            class_name="test_class",
        ),
    )

    assert resources.collection_classes == {"test_name": patched_proxy.return_value}
    patched_proxy.assert_called_once_with(
        settings=core.CollectionClassSettings(
            module="test_module",
            class_name="test_class",
        )
    )


def test_add_transfer_class(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.TransferClassProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.transfer_classes == {}

    resources.add_transfer_class(
        name="test_name",
        settings=app.TransferClassSettings(
            module="test_module",
            class_name="test_class",
        ),
    )

    assert resources.transfer_classes == {"test_name": patched_proxy.return_value}
    patched_proxy.assert_called_once_with(
        settings=core.TransferClassSettings(
            module="test_module",
            class_name="test_class",
        )
    )


def test_add_source(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.SourceProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.sources == {}

    resources.add_source(
        name="test_name",
        settings=app.SourceSettings(
            class_name="test_class",
            init_args={"test_key": "test_value"},
        ),
    )

    assert resources.sources == {"test_name": patched_proxy.return_value}


def test_add_destination(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.DestinationProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.destinations == {}

    resources.add_destination(
        name="test_name",
        settings=app.DestinationSettings(
            class_name="test_class",
            init_args={"test_key": "test_value"},
        ),
    )

    assert resources.destinations == {"test_name": patched_proxy.return_value}


def test_add_collection(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.CollectionProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.collections == {}

    resources.add_collection(
        name="test_name",
        settings=app.CollectionSettings(
            class_name="test_class",
            init_args={"test_key": "test_value"},
        ),
    )

    assert resources.collections == {"test_name": patched_proxy.return_value}


def test_add_transfer(mocker: pytest_mock.MockerFixture):
    patched_proxy = mocker.patch("secret_transfer.core.TransferProxy.from_settings")

    resources = app.ApplicationResources()
    assert resources.transfers == {}

    resources.add_transfer(
        name="test_name",
        settings=app.TransferSettings(
            class_name="test_class",
            init_args={"test_key": "test_value"},
        ),
    )

    assert resources.transfers == {"test_name": patched_proxy.return_value}
