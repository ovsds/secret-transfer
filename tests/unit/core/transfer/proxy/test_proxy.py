import typing

import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource.suite as test_suite


class TestTransferProxy(test_suite.ResourceProxySuite[protocol.TransferProtocol]):
    @pytest.fixture(name="collection")
    def fixture_collection(self) -> type[protocol.TransferProtocol]:
        class TestTransfer(core.AbstractTransfer):
            __register__ = False

        return TestTransfer

    @pytest.fixture(name="target_proxy")
    def fixture_target_proxy(self) -> type[core.TransferProxy]:
        return core.TransferProxy

    @pytest.fixture(name="target_settings")
    def fixture_target_settings(self) -> type[core.TransferSettings]:
        return core.TransferSettings

    @pytest.fixture(name="classes")
    def fixture_classes(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        class_name: str,
        collection: type[protocol.TransferProtocol],
    ) -> typing.Mapping[str, type[protocol.TransferProtocol]]:
        return {class_name: collection}

    @pytest.fixture(name="default_class")
    def fixture_default_class(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, collection: type[protocol.TransferProtocol]
    ) -> type[protocol.TransferProtocol]:
        return collection

    @pytest.fixture(name="class_name")
    def fixture_class_name(self) -> str:
        return "TestTransfer"
