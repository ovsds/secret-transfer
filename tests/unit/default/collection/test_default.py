import pytest
import pytest_mock

import secret_transfer
import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.utils as test_utils

TEST_KEY = "test_key"
TEST_VALUE = "test_value"
TEST_SOURCE_KEY = "test_source_key"
TEST_SOURCE_NAME = "test_source_name"


def test_registered():
    key = secret_transfer.DefaultCollection.__name__
    assert key in core.CollectionRegistry.classes
    assert core.CollectionRegistry.classes[key] is secret_transfer.DefaultCollection
    assert core.CollectionRegistry.default_class is secret_transfer.DefaultCollection


def test_parse_init_arguments():
    test_source = test_utils.MagicMock(spec=protocol.SourceProtocol)

    arguments = secret_transfer.DefaultCollection.parse_init_arguments(
        **{
            TEST_KEY: {
                "source": test_source,
                "key": TEST_SOURCE_KEY,
            },
        }
    )

    assert arguments == {
        TEST_KEY: secret_transfer.DefaultCollectionItem(
            source=test_source,
            key=TEST_SOURCE_KEY,
        ),
    }


@pytest.fixture(name="test_source")
def fixture_test_source(mocker: pytest_mock.MockerFixture) -> test_utils.MagicMock:
    test_source = mocker.MagicMock(spec=protocol.SourceProtocol)
    return test_source


def test_get(test_source: test_utils.MagicMock):
    test_source.__getitem__.return_value = TEST_VALUE

    collection = secret_transfer.DefaultCollection(
        **{
            TEST_KEY: secret_transfer.DefaultCollectionItem(
                source=test_source,
                key=TEST_SOURCE_KEY,
            ),
        },
    )

    assert collection[TEST_KEY] == TEST_VALUE
    test_source.__getitem__.assert_called_once_with(TEST_SOURCE_KEY)


def test_get_without_source_key(test_source: test_utils.MagicMock):
    test_source.__getitem__.return_value = TEST_VALUE

    collection = secret_transfer.DefaultCollection(
        **{
            TEST_SOURCE_KEY: secret_transfer.DefaultCollectionItem(
                source=test_source,
            ),
        },
    )

    assert collection[TEST_SOURCE_KEY] == TEST_VALUE
    test_source.__getitem__.assert_called_once_with(TEST_SOURCE_KEY)


def test_get_no_key(test_source: test_utils.MagicMock):
    collection = secret_transfer.DefaultCollection(
        **{
            "another_key": secret_transfer.DefaultCollectionItem(
                source=test_source,
                key=TEST_SOURCE_KEY,
            ),
        },
    )

    with pytest.raises(secret_transfer.DefaultCollection.KeyNotFoundError):
        collection[TEST_KEY]
    test_source.__getitem__.assert_not_called()


def test_get_no_key_in_source(test_source: test_utils.MagicMock):
    test_source.__getitem__.side_effect = protocol.SourceProtocol.KeyNotFoundError

    collection = secret_transfer.DefaultCollection(
        **{
            TEST_KEY: secret_transfer.DefaultCollectionItem(
                source=test_source,
                key=TEST_SOURCE_KEY,
            ),
        },
    )

    with pytest.raises(secret_transfer.DefaultCollection.KeyNotFoundError):
        collection[TEST_KEY]
    test_source.__getitem__.assert_called_once_with(TEST_SOURCE_KEY)


def test_iter(test_source: test_utils.MagicMock):
    collection = secret_transfer.DefaultCollection(
        **{
            TEST_KEY: secret_transfer.DefaultCollectionItem(
                source=test_source,
                key=TEST_SOURCE_KEY,
            ),
        },
    )

    assert list(collection) == [TEST_KEY]
    test_source.assert_not_called()


def test_items(test_source: test_utils.MagicMock):
    test_source.__getitem__.return_value = TEST_VALUE

    collection = secret_transfer.DefaultCollection(
        **{
            TEST_KEY: secret_transfer.DefaultCollectionItem(
                source=test_source,
                key=TEST_SOURCE_KEY,
            ),
        },
    )

    assert list(collection.items()) == [(TEST_KEY, TEST_VALUE)]
    test_source.__getitem__.assert_called_once_with(TEST_SOURCE_KEY)


def test_items_no_key_in_source(test_source: test_utils.MagicMock):
    test_source.__getitem__.side_effect = protocol.SourceProtocol.KeyNotFoundError

    collection = secret_transfer.DefaultCollection(
        **{
            TEST_KEY: secret_transfer.DefaultCollectionItem(
                source=test_source,
                key=TEST_SOURCE_KEY,
            ),
        },
    )

    with pytest.raises(secret_transfer.DefaultCollection.KeyNotFoundError):
        list(collection.items())
    test_source.__getitem__.assert_called_once_with(TEST_SOURCE_KEY)
