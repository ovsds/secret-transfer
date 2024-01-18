import typing

import pytest

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol


class ClassProxySuite(typing.Generic[protocol.ResourceType]):
    @pytest.fixture(name="target_class_proxy")
    def fixture_target_class_proxy(self) -> type[core_base.BaseClassProxy[protocol.ResourceType]]:
        raise NotImplementedError

    @pytest.fixture(name="target_class")
    def fixture_target_class(self) -> type[protocol.ResourceType]:
        raise NotImplementedError

    @pytest.fixture(name="target_class_module")
    def fixture_target_class_module(self, target_class: type[protocol.ResourceType]) -> str:
        return target_class.__module__

    @pytest.fixture(name="target_class_name")
    def fixture_target_class_name(self, target_class: type[protocol.ResourceType]) -> str:
        return target_class.__name__

    @pytest.fixture(name="invalid_protocol_class_name")
    def fixture_invalid_protocol_class_name(self) -> str:
        raise NotImplementedError

    @pytest.fixture(name="instance_arguments")
    def fixture_instance_arguments(self) -> dict[str, typing.Any]:
        return {}

    def test_default(
        self,
        target_class_proxy: type[core_base.BaseClassProxy[protocol.ResourceType]],
        target_class: type[protocol.ResourceType],
        target_class_module: str,
        target_class_name: str,
        instance_arguments: dict[str, typing.Any],
    ):
        proxy_class = target_class_proxy.from_settings(
            settings=core_base.ResourceClassSettings(
                module=target_class_module,
                class_name=target_class_name,
            )
        )
        proxy = proxy_class(**instance_arguments)

        assert isinstance(proxy, target_class)

    def test_not_existing_module(
        self,
        target_class_proxy: type[core_base.BaseClassProxy[protocol.ResourceType]],
        target_class_name: str,
        instance_arguments: dict[str, typing.Any],
    ):
        proxy_class = target_class_proxy.from_settings(
            settings=core_base.ResourceClassSettings(
                module="not_existing_module",
                class_name=target_class_name,
            )
        )

        with pytest.raises(target_class_proxy.ImportError):
            proxy_class(**instance_arguments)

    def test_not_existing_class(
        self,
        target_class_proxy: type[core_base.BaseClassProxy[protocol.ResourceType]],
        target_class_module: str,
        instance_arguments: dict[str, typing.Any],
    ):
        proxy_class = target_class_proxy.from_settings(
            settings=core_base.ResourceClassSettings(
                module=target_class_module,
                class_name="NotExistingClass",
            )
        )

        with pytest.raises(target_class_proxy.ImportError):
            proxy_class(**instance_arguments)

    def test_not_implementing_protocol(
        self,
        target_class_proxy: type[core_base.BaseClassProxy[protocol.ResourceType]],
        target_class_module: str,
        invalid_protocol_class_name: str,
        instance_arguments: dict[str, typing.Any],
    ):
        proxy_class = target_class_proxy.from_settings(
            settings=core_base.ResourceClassSettings(
                module=target_class_module,
                class_name=invalid_protocol_class_name,
            )
        )

        with pytest.raises(target_class_proxy.InvalidProtocolError):
            proxy_class(**instance_arguments)
