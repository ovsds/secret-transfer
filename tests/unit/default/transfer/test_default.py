import pytest
import pytest_mock

import secret_transfer
import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.utils as test_utils

TEST_KEY = "test_key"
TEST_VALUE = "test_value"
TEST_COLLECTION_NAME = "test_collection"
TEST_DESTINATION_NAME = "test_destination"


def test_registered():
    key = secret_transfer.DefaultTransfer.__name__
    assert key in core.TransferRegistry.classes
    assert core.TransferRegistry.classes[key] is secret_transfer.DefaultTransfer
    assert core.TransferRegistry.default_class is secret_transfer.DefaultTransfer


def test_parse_init_arguments():
    test_collection = test_utils.MagicMock(spec=protocol.CollectionProtocol)
    test_destination = test_utils.MagicMock(spec=protocol.DestinationProtocol)

    arguments = secret_transfer.DefaultTransfer.parse_init_arguments(
        **{
            "collection": test_collection,
            "destination": test_destination,
        }
    )

    assert arguments == {
        "collection": test_collection,
        "destination": test_destination,
    }


@pytest.fixture(name="test_collection")
def fixture_test_collection(mocker: pytest_mock.MockerFixture) -> test_utils.MagicMock:
    test_collection = mocker.MagicMock(spec=protocol.CollectionProtocol)
    return test_collection


@pytest.fixture(name="test_destination")
def fixture_test_destination(mocker: pytest_mock.MockerFixture) -> test_utils.Mock:
    test_destination = mocker.MagicMock(spec=protocol.DestinationProtocol)
    return test_destination


def test_run(test_collection: test_utils.Mock, test_destination: test_utils.Mock):
    test_collection.items.return_value = [
        (TEST_KEY, TEST_VALUE),
    ]

    transfer = secret_transfer.DefaultTransfer(
        collection=test_collection,
        destination=test_destination,
    )

    transfer.run()
    test_collection.items.assert_called_once_with()
    test_destination.__setitem__.assert_has_calls(
        calls=[
            ((TEST_KEY, TEST_VALUE), {}),
        ],
        any_order=True,
    )


def test_run_collection_error(
    test_collection: test_utils.Mock,
    test_destination: test_utils.Mock,
):
    test_collection.items.side_effect = protocol.CollectionProtocol.BaseError

    transfer = secret_transfer.DefaultTransfer(
        collection=test_collection,
        destination=test_destination,
    )

    with pytest.raises(secret_transfer.DefaultTransfer.CollectionError):
        transfer.run()

    test_destination.__setitem__.assert_not_called()


def test_clean(test_collection: test_utils.Mock, test_destination: test_utils.Mock):
    test_collection.__iter__.return_value = [TEST_KEY]

    transfer = secret_transfer.DefaultTransfer(
        collection=test_collection,
        destination=test_destination,
    )
    transfer.clean()
    test_collection.__iter__.assert_called_once_with()
    test_destination.__delitem__.assert_has_calls(
        calls=[
            ((TEST_KEY,), {}),
        ],
        any_order=True,
    )
