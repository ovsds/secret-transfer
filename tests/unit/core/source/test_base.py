import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractSource.__name__ not in core.SourceRegistry.classes


def test_register():
    class TestSource(core.AbstractSource):
        __register__ = False

    source = TestSource()

    assert "test" not in core.SourceRegistry.instances
    source.register("test")
    assert "test" in core.SourceRegistry.instances
    assert core.SourceRegistry.instances["test"] == source
