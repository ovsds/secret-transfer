import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractDestination.__name__ not in core.DestinationRegistry.classes


def test_register():
    class TestDestination(core.AbstractDestination):
        __register__ = False

    destination = TestDestination()

    assert "test" not in core.DestinationRegistry.instances
    destination.register("test")
    assert "test" in core.DestinationRegistry.instances
    assert core.DestinationRegistry.instances["test"] == destination
