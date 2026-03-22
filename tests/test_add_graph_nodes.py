import networkx as nx
import pytest
from src.syncspec.add_graph_nodes_context import AddGraphNodesContext
from src.syncspec.add_graph_nodes_parameter import AddGraphNodesParameter
from src.syncspec.add_graph_nodes import make_add_graph_nodes


@pytest.mark.parametrize("directive_type,key,line_number,name", [
    ("import", "sys", 1, "main.py"),
    ("class", "MyClass", 10, "module.py"),
])
def test_add_graph_nodes(directive_type, key, line_number, name):
    context = AddGraphNodesContext(G=nx.DiGraph())
    add_func = make_add_graph_nodes(context)
    param = AddGraphNodesParameter(directive_type, key, line_number, name)

    add_func(param)

    node_id = f"{directive_type}_{name}_{line_number}"
    assert node_id in context.G
    attrs = context.G.nodes[node_id]
    assert attrs["directive_type"] == directive_type
    assert attrs["key"] == key
    assert attrs["line_number"] == line_number
    assert attrs["file_name"] == name