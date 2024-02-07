import typing

import pytest
import typing_extensions

import secret_transfer.core.base as core_base


class ResourceTestProtocol(typing.Protocol):
    ...


Registry = core_base.BaseRegistry[ResourceTestProtocol]  # pyright: ignore[reportGeneralTypeIssues]
RegistryType = type[Registry]


class ClassBase:
    @classmethod
    def get_default_instances(cls) -> dict[str, typing_extensions.Self]:
        return {}


@pytest.fixture(name="registry1")
def fixture_registry1() -> RegistryType:
    class Registry1(Registry):
        ...

    return Registry1


@pytest.fixture(name="registry2")
def fixture_registry2() -> RegistryType:
    class Registry2(Registry):
        ...

    return Registry2


def test_multiple_registry_have_different_defaults(registry1: RegistryType, registry2: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        __register__ = True

    class Class2(ClassBase, metaclass=registry2):
        __register__ = True

    assert Class1.__name__ in registry1.classes
    assert Class2.__name__ in registry2.classes
    assert Class1.__name__ not in registry2.classes
    assert Class2.__name__ not in registry1.classes


def test_explicit_class_registration(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        __register__ = True

    assert Class1.__name__ in registry1.classes
    assert registry1.classes[Class1.__name__] is Class1


def test_implicit_class_registration(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        ...

    assert Class1.__name__ in registry1.classes
    assert registry1.classes[Class1.__name__] is Class1


def test_explicit_class_non_registration(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        __register__ = False

    assert Class1.__name__ not in registry1.classes


def test_class_name_collision(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):  # pyright: ignore[reportUnusedClass, reportGeneralTypeIssues]
        __register__ = True

    with pytest.raises(ValueError):

        class Class1(ClassBase, metaclass=registry1):  # noqa: F811 # pyright: ignore[reportUnusedClass]
            __register__ = True


def test_instance_registration(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        ...

    name = "test_name"

    test_instance = Class1()
    registry1.register_instance(name, test_instance)

    assert name in registry1.instances
    assert registry1.instances[name] is test_instance


def test_instance_name_collision(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        ...

    name = "test_name"

    test_instance = Class1()
    registry1.register_instance(name, test_instance)

    test_instance2 = Class1()
    with pytest.raises(ValueError):
        registry1.register_instance(name, test_instance2)


def test_default_class_registration(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        ...

    registry1.register_default_class(Class1)

    assert registry1.default_class is Class1


def test_default_class_registration_using_attribute(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        __default__ = True

    assert registry1.default_class is Class1


def test_default_class_collision(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        ...

    class Class2(ClassBase, metaclass=registry1):
        ...

    registry1.register_default_class(Class1)
    with pytest.raises(ValueError):
        registry1.register_default_class(Class2)


def test_default_class_collision_force(registry1: RegistryType):
    class Class1(ClassBase, metaclass=registry1):
        ...

    class Class2(ClassBase, metaclass=registry1):
        ...

    registry1.register_default_class(Class1)

    registry1.register_default_class(Class2, force=True)

    assert registry1.default_class is Class2


def test_default_instance_registration(registry1: RegistryType):
    class Class1(metaclass=registry1):
        @classmethod
        def get_default_instances(cls) -> dict[str, ResourceTestProtocol]:
            return {"test_name": cls()}

    assert "test_name" in registry1.instances
    assert isinstance(registry1.instances["test_name"], Class1)


def test_default_instance_collision(registry1: RegistryType):
    class Class1(metaclass=registry1):  # pyright: ignore[reportUnusedClass]
        @classmethod
        def get_default_instances(cls) -> dict[str, ResourceTestProtocol]:
            return {"test_name": cls()}

    with pytest.raises(ValueError):

        class Class2(metaclass=registry1):  # pyright: ignore[reportUnusedClass]
            @classmethod
            def get_default_instances(cls) -> dict[str, ResourceTestProtocol]:
                return {"test_name": cls()}
