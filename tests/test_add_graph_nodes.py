import pytest
import networkx as nx
from src.syncspec.add_graph_nodes import make_add_graph_nodes
from src.syncspec.add_graph_nodes_context import AddGraphNodesContext
from src.syncspec.node import Node
from src.syncspec.graph_node import GraphNode


@pytest.mark.parametrize(
    "dtype,key,line,name",
    [
        ("import", "sys", 1, "main.py"),
        ("class", "MyClass", 10, "utils.py"),
    ],
)
def test_add_graph_nodes(dtype, key, line, name):
    G = nx.DiGraph()
    context = AddGraphNodesContext(G=G)
    add_fn = make_add_graph_nodes(context)
    node = Node(directive_type=dtype, key=key, line_number=line, name=name)

    result = add_fn(node)
    node_id = f"{dtype}_{name}_{line}"

    assert isinstance(result, GraphNode)
    assert result.directive_type == dtype
    assert result.key == key
    assert result.line_number == line
    assert result.name == name
    assert G.has_node(node_id)

    attrs = G.nodes[node_id]
    assert attrs["directive_type"] == dtype
    assert attrs["key"] == key
    assert attrs["line_number"] == line
    assert attrs["file_name"] == name