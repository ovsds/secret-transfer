import typing

import pydantic

import secret_transfer.core as core
import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol
import secret_transfer.utils.pydantic as pydantic_utils


class ClassSettings(pydantic_utils.BaseModel, typing.Generic[protocol.ResourceType]):
    module: str
    class_name: str

    def to_proxy_settings(self) -> core_base.ResourceClassSettings[protocol.ResourceType]:
        return self._proxy_settings_class(
            module=self.module,
            class_name=self.class_name,
        )

    @property
    def _proxy_settings_class(self) -> type[core_base.ResourceClassSettings[protocol.ResourceType]]:
        raise NotImplementedError


class SourceClassSettings(ClassSettings[protocol.SourceProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.SourceClassSettings]:
        return core.SourceClassSettings


class DestinationClassSettings(ClassSettings[protocol.DestinationProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.DestinationClassSettings]:
        return core.DestinationClassSettings


class CollectionClassSettings(ClassSettings[protocol.CollectionProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.CollectionClassSettings]:
        return core.CollectionClassSettings


class TransferClassSettings(ClassSettings[protocol.TransferProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.TransferClassSettings]:
        return core.TransferClassSettings


class ResourceSettings(pydantic_utils.BaseModel, typing.Generic[protocol.ResourceType]):
    class_name: typing.Optional[str] = None
    init_args: dict[str, typing.Any] = pydantic.Field(default_factory=dict)

    def to_proxy_settings(
        self,
        resource_classes: typing.Mapping[str, type[protocol.ResourceType]],
        default_resource_class: typing.Optional[type[protocol.ResourceType]],
        resources: typing.Mapping[str, typing.Mapping[str, protocol.BaseResourceProtocol]],
    ) -> core_base.ResourceSettings[protocol.ResourceType]:
        return self._proxy_settings_class(
            resource_classes=resource_classes,
            default_resource_class=default_resource_class,
            resources=resources,
            class_name=self.class_name,
            raw_arguments=self.init_args,
        )

    @property
    def _proxy_settings_class(self) -> type[core_base.ResourceSettings[protocol.ResourceType]]:
        raise NotImplementedError


class SourceSettings(ResourceSettings[protocol.SourceProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.SourceSettings]:
        return core.SourceSettings


class DestinationSettings(ResourceSettings[protocol.DestinationProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.DestinationSettings]:
        return core.DestinationSettings


class CollectionSettings(ResourceSettings[protocol.CollectionProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.CollectionSettings]:
        return core.CollectionSettings


class TransferSettings(ResourceSettings[protocol.TransferProtocol]):
    @property
    def _proxy_settings_class(self) -> type[core.TransferSettings]:
        return core.TransferSettings


class ApplicationSettings(pydantic_utils.BaseModel):
    source_classes: dict[str, SourceClassSettings] = pydantic.Field(default_factory=dict)
    destination_classes: dict[str, DestinationClassSettings] = pydantic.Field(default_factory=dict)
    collection_classes: dict[str, CollectionClassSettings] = pydantic.Field(default_factory=dict)
    transfer_classes: dict[str, TransferClassSettings] = pydantic.Field(default_factory=dict)

    sources: dict[str, SourceSettings] = pydantic.Field(default_factory=dict)
    destinations: dict[str, DestinationSettings] = pydantic.Field(default_factory=dict)
    collections: dict[str, CollectionSettings] = pydantic.Field(default_factory=dict)
    transfers: dict[str, TransferSettings] = pydantic.Field(default_factory=dict)
