import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractTransfer.__name__ not in core.TransferRegistry.classes
