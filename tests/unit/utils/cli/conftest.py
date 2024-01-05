import pytest
import pytest_mock

import tests.utils as test_utils


@pytest.fixture(name="run_command_mock")
def fixture_run_command_mock(mocker: pytest_mock.MockFixture) -> test_utils.Mock:
    return mocker.patch("secret_transfer.utils.cli.base.run")
