import pytest
from unittest.mock import MagicMock
from simplibs.exception import ParamError
from simplibs.regex.base_class import Regex
from simplibs.regex.containers._helpers.flatten_nodes import flatten_nodes


class DummyRegex(Regex):
    def __init__(self, name: str = "dummy") -> None:
        self.name = name

    def to_pattern(self) -> str:
        return self.name


class ContainerA(Regex):
    def __init__(self, nodes: list[Regex]) -> None:
        self.nodes = tuple(nodes)

    def to_pattern(self) -> str:
        return "".join(n.to_pattern() for n in self.nodes)


class ContainerB(Regex):
    def __init__(self, nodes: list[Regex]) -> None:
        self.nodes = tuple(nodes)

    def to_pattern(self) -> str:
        return "".join(n.to_pattern() for n in self.nodes)


def test_flatten_nodes_basic() -> None:
    """Verify that flatten_nodes leaves regular Regex instances untouched."""
    n1 = DummyRegex("a")
    n2 = DummyRegex("b")

    result = flatten_nodes([n1, n2], ContainerA, "ContainerA")

    assert result == [n1, n2]


def test_flatten_nodes_nested_same_type() -> None:
    """Verify that nested instances of the exact container_type are flattened."""
    inner1 = DummyRegex("a")
    inner2 = DummyRegex("b")
    nested_container = ContainerA([inner1, inner2])

    normal_node = DummyRegex("c")

    result = flatten_nodes([nested_container, normal_node], ContainerA, "ContainerA")

    assert result == [inner1, inner2, normal_node]


def test_flatten_nodes_subclass_or_different_type_not_unwrapped() -> None:
    """Verify that different container types or subclasses are NOT unwrapped (exact type check)."""
    inner = DummyRegex("a")
    container_b_instance = ContainerB([inner])

    result = flatten_nodes([container_b_instance], ContainerA, "ContainerA")

    assert len(result) == 1
    assert result[0] is container_b_instance


def test_flatten_nodes_raises_on_invalid_node() -> None:
    """Verify that flatten_nodes raises ParamError if an item is not a Regex instance."""
    valid_node = DummyRegex("a")
    invalid_item = "not_a_regex"

    with pytest.raises(ParamError) as exc_info:
        flatten_nodes([valid_node, invalid_item], ContainerA, "ContainerA")

    assert exc_info.value.error_name == "NODE_NOT_REGEX_ERROR"