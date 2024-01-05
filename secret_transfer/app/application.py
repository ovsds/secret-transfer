import dataclasses
import typing

import typing_extensions

import secret_transfer.app.settings as app_settings
import secret_transfer.core as core
import secret_transfer.protocol as protocol

SourceClassesType = typing.MutableMapping[str, type[protocol.SourceProtocol]]
DestinationClassesType = typing.MutableMapping[str, type[protocol.DestinationProtocol]]
CollectionClassesType = typing.MutableMapping[str, type[protocol.CollectionProtocol]]
TransferClassesType = typing.MutableMapping[str, type[protocol.TransferProtocol]]

SourcesType = typing.MutableMapping[str, protocol.SourceProtocol]
DestinationsType = typing.MutableMapping[str, protocol.DestinationProtocol]
CollectionsType = typing.MutableMapping[str, protocol.CollectionProtocol]
TransfersType = typing.MutableMapping[str, protocol.TransferProtocol]


@dataclasses.dataclass
class ApplicationResources:
    source_classes: SourceClassesType = dataclasses.field(default_factory=dict)
    destination_classes: DestinationClassesType = dataclasses.field(default_factory=dict)
    collection_classes: CollectionClassesType = dataclasses.field(default_factory=dict)
    transfer_classes: TransferClassesType = dataclasses.field(default_factory=dict)

    default_source_class: typing.Optional[type[protocol.SourceProtocol]] = None
    default_destination_class: typing.Optional[type[protocol.DestinationProtocol]] = None
    default_collection_class: typing.Optional[type[protocol.CollectionProtocol]] = None
    default_transfer_class: typing.Optional[type[protocol.TransferProtocol]] = None

    sources: SourcesType = dataclasses.field(default_factory=dict)
    destinations: DestinationsType = dataclasses.field(default_factory=dict)
    collections: CollectionsType = dataclasses.field(default_factory=dict)
    transfers: TransfersType = dataclasses.field(default_factory=dict)

    @classmethod
    def from_registry(cls):
        return cls(
            source_classes=core.SourceRegistry.classes.copy(),
            destination_classes=core.DestinationRegistry.classes.copy(),
            collection_classes=core.CollectionRegistry.classes.copy(),
            transfer_classes=core.TransferRegistry.classes.copy(),
            default_source_class=core.SourceRegistry.default_class,
            default_destination_class=core.DestinationRegistry.default_class,
            default_collection_class=core.CollectionRegistry.default_class,
            default_transfer_class=core.TransferRegistry.default_class,
            sources=core.SourceRegistry.instances.copy(),
            destinations=core.DestinationRegistry.instances.copy(),
            collections=core.CollectionRegistry.instances.copy(),
            transfers=core.TransferRegistry.instances.copy(),
        )

    def add_source_class(self, name: str, settings: app_settings.SourceClassSettings):
        self.source_classes[name] = core.SourceClassProxy.from_settings(settings=settings.to_proxy_settings())

    def add_destination_class(self, name: str, settings: app_settings.DestinationClassSettings):
        self.destination_classes[name] = core.DestinationClassProxy.from_settings(settings=settings.to_proxy_settings())

    def add_collection_class(self, name: str, settings: app_settings.CollectionClassSettings):
        self.collection_classes[name] = core.CollectionClassProxy.from_settings(settings=settings.to_proxy_settings())

    def add_transfer_class(self, name: str, settings: app_settings.TransferClassSettings):
        self.transfer_classes[name] = core.TransferClassProxy.from_settings(settings=settings.to_proxy_settings())

    def _resources_dict(self) -> typing.Mapping[str, typing.Mapping[str, protocol.BaseResourceProtocol]]:
        return {
            "sources": self.sources,
            "destinations": self.destinations,
            "collections": self.collections,
            "transfers": self.transfers,
        }

    def add_source(self, name: str, settings: app_settings.SourceSettings):
        self.sources[name] = core.SourceProxy.from_settings(
            settings=settings.to_proxy_settings(
                resource_classes=self.source_classes,
                default_resource_class=self.default_source_class,
                resources=self._resources_dict(),
            )
        )

    def add_destination(self, name: str, settings: app_settings.DestinationSettings):
        self.destinations[name] = core.DestinationProxy.from_settings(
            settings=settings.to_proxy_settings(
                resource_classes=self.destination_classes,
                default_resource_class=self.default_destination_class,
                resources=self._resources_dict(),
            )
        )

    def add_collection(self, name: str, settings: app_settings.CollectionSettings):
        self.collections[name] = core.CollectionProxy.from_settings(
            settings=settings.to_proxy_settings(
                resource_classes=self.collection_classes,
                default_resource_class=self.default_collection_class,
                resources=self._resources_dict(),
            )
        )

    def add_transfer(self, name: str, settings: app_settings.TransferSettings):
        self.transfers[name] = core.TransferProxy.from_settings(
            settings=settings.to_proxy_settings(
                resource_classes=self.transfer_classes,
                default_resource_class=self.default_transfer_class,
                resources=self._resources_dict(),
            )
        )


class Application:
    def __init__(self, resources: ApplicationResources):
        self.resources = resources

    @classmethod
    def from_settings(
        cls,
        settings: app_settings.ApplicationSettings,
        exclude_registry: bool = False,
    ) -> typing_extensions.Self:
        if exclude_registry:
            resources = ApplicationResources()
        else:
            resources = ApplicationResources.from_registry()

        for name, class_settings in settings.source_classes.items():
            resources.add_source_class(name=name, settings=class_settings)
        for name, class_settings in settings.destination_classes.items():
            resources.add_destination_class(name=name, settings=class_settings)
        for name, class_settings in settings.collection_classes.items():
            resources.add_collection_class(name=name, settings=class_settings)
        for name, class_settings in settings.transfer_classes.items():
            resources.add_transfer_class(name=name, settings=class_settings)

        for name, source_settings in settings.sources.items():
            resources.add_source(name=name, settings=source_settings)
        for name, destination_settings in settings.destinations.items():
            resources.add_destination(name=name, settings=destination_settings)
        for name, collection_settings in settings.collections.items():
            resources.add_collection(name=name, settings=collection_settings)
        for name, transfer_settings in settings.transfers.items():
            resources.add_transfer(name=name, settings=transfer_settings)

        return cls(resources=resources)

    def run(self, transfer_name: str) -> None:
        self.resources.transfers[transfer_name].run()

    def run_all(self) -> None:
        for transfer in self.resources.transfers.values():
            transfer.run()

    def clean(self, transfer_name: str) -> None:
        self.resources.transfers[transfer_name].clean()

    def clean_all(self) -> None:
        for transfer in self.resources.transfers.values():
            transfer.clean()
