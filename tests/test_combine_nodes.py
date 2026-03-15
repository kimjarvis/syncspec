import pytest
import networkx as nx
from src.syncspec.node import Node
from src.syncspec.edge import Edge
from src.syncspec.combine_nodes_context import CombineNodesContext
from src.syncspec.combine_nodes import make_combine_nodes


@pytest.mark.parametrize("dtype, color", [
    ("source", "lightblue"), ("export", "red"), ("include", "lightgreen"), ("import", "yellow")
])
def test_graph_node_and_return_object(dtype, color):
    ctx = CombineNodesContext(G=nx.DiGraph())
    combine = make_combine_nodes(ctx)
    node = Node(dtype, "k1", 10, "mod")

    result = combine(node)

    nid = f"{dtype}_mod_10"
    assert nid in ctx.G
    assert ctx.G.nodes[nid]["fillcolor"] == color
    assert ctx.G.nodes[nid]["label"] == f"{dtype}\nmod\n:10"
    assert isinstance(result, Edge)
    assert result.directive_type == dtype
    assert result.key == "k1"