import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractSource.__name__ not in core.SourceRegistry.classes


def test_register():
    class TestSource(core.AbstractSource):
        __register__ = False

    name = "test_name"

    test_source = TestSource()
    test_source.register(name)

    assert name in core.SourceRegistry.instances
    assert test_source is core.SourceRegistry.instances[name]
