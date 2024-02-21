import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractCollection.__name__ not in core.CollectionRegistry.classes


def test_register():
    class TestCollection(core.AbstractCollection):
        __register__ = False

    collection = TestCollection()

    assert "test" not in core.CollectionRegistry.instances
    collection.register("test")
    assert "test" in core.CollectionRegistry.instances
    assert core.CollectionRegistry.instances["test"] == collection
