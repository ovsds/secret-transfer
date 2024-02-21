import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractTransfer.__name__ not in core.TransferRegistry.classes


def test_register():
    class TestTransfer(core.AbstractTransfer):
        __register__ = False

    transfer = TestTransfer()

    assert "test" not in core.TransferRegistry.instances
    transfer.register("test")
    assert "test" in core.TransferRegistry.instances
    assert core.TransferRegistry.instances["test"] == transfer
