import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractCollection.__name__ not in core.CollectionRegistry.classes


def test_register():
    class TestCollection(core.AbstractCollection):
        __register__ = False

    name = "test_name"

    test_source = TestCollection()
    test_source.register(name)

    assert name in core.CollectionRegistry.instances
    assert test_source is core.CollectionRegistry.instances[name]
