import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractDestination.__name__ not in core.DestinationRegistry.classes


def test_register():
    class TestDestination(core.AbstractDestination):
        __register__ = False

    name = "test_name"

    test_source = TestDestination()
    test_source.register(name)

    assert name in core.DestinationRegistry.instances
    assert test_source is core.DestinationRegistry.instances[name]
