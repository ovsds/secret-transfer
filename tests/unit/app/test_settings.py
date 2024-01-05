import secret_transfer


def test_from_yaml_empty():
    settings = secret_transfer.ApplicationSettings.from_yaml("")
    assert settings == secret_transfer.ApplicationSettings()


def test_from_yaml():
    settings = secret_transfer.ApplicationSettings.from_yaml(
        """
        source_classes:
          TestSource:
            module: test_source_module
            class_name: TestSourceClass

        destination_classes:
          TestDestination:
            module: test_destination_module
            class_name: TestDestinationClass

        collection_classes:
          TestCollection:
            module: test_collection_module
            class_name: TestCollectionClass

        transfer_classes:
          TestTransfer:
            module: test_transfer_module
            class_name: TestTransferClass

        sources:
          TestSource:
            class_name: TestSource
            init_args:
              test_arg: test_value

        destinations:
          TestDestination:
            class_name: TestDestination
            init_args:
              test_arg: test_value

        collections:
          TestCollection:
            class_name: TestCollection
            init_args:
              test_arg: test_value

        transfers:
          TestTransfer:
            class_name: TestTransfer
            init_args:
              test_arg: test_value
        """
    )

    assert settings.source_classes == {
        "TestSource": secret_transfer.SourceClassSettings(
            module="test_source_module",
            class_name="TestSourceClass",
        )
    }

    assert settings.destination_classes == {
        "TestDestination": secret_transfer.DestinationClassSettings(
            module="test_destination_module",
            class_name="TestDestinationClass",
        )
    }

    assert settings.collection_classes == {
        "TestCollection": secret_transfer.CollectionClassSettings(
            module="test_collection_module",
            class_name="TestCollectionClass",
        )
    }

    assert settings.transfer_classes == {
        "TestTransfer": secret_transfer.TransferClassSettings(
            module="test_transfer_module",
            class_name="TestTransferClass",
        )
    }

    assert settings.sources == {
        "TestSource": secret_transfer.SourceSettings(
            class_name="TestSource",
            init_args={
                "test_arg": "test_value",
            },
        )
    }

    assert settings.destinations == {
        "TestDestination": secret_transfer.DestinationSettings(
            class_name="TestDestination",
            init_args={
                "test_arg": "test_value",
            },
        )
    }

    assert settings.collections == {
        "TestCollection": secret_transfer.CollectionSettings(
            class_name="TestCollection",
            init_args={
                "test_arg": "test_value",
            },
        )
    }

    assert settings.transfers == {
        "TestTransfer": secret_transfer.TransferSettings(
            class_name="TestTransfer",
            init_args={
                "test_arg": "test_value",
            },
        )
    }


def test_from_yaml_resource_init_args():
    settings = secret_transfer.ApplicationSettings.from_yaml(
        """
        sources:
          TestSource:
            class_name: TestSource
            init_args:
              str_arg: test_value
              int_arg: 1
              float_arg: 1.0
              bool_arg: true
              list_arg:
                - value1
                - value2
              dict_arg:
                test_key: test_value
        """
    )

    assert settings.sources == {
        "TestSource": secret_transfer.SourceSettings(
            class_name="TestSource",
            init_args={
                "str_arg": "test_value",
                "int_arg": 1,
                "float_arg": 1.0,
                "bool_arg": True,
                "list_arg": ["value1", "value2"],
                "dict_arg": {"test_key": "test_value"},
            },
        )
    }
