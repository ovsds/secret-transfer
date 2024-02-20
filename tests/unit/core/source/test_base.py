import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractSource.__name__ not in core.SourceRegistry.classes
