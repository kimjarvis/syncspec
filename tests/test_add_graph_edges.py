import networkx as nx
import pytest
from src.syncspec.add_graph_edges_context import AddGraphEdgesContext
from src.syncspec.graph_node import GraphNode
from src.syncspec.add_graph_edges import make_add_graph_edges


@pytest.mark.parametrize("dir_type, src_type, key_match, expected_edges", [
    ("include", "source", True, 1),
    ("include", "source", False, 0),
    ("import", "export", True, 1),
    ("import", "export", False, 0),
    ("other", None, True, 0),
])
def test_add_graph_edges(dir_type, src_type, key_match, expected_edges):
    G = nx.DiGraph()
    key = "test_key"

    # Add source node to graph
    if src_type:
        G.add_node("src_id", directive_type=src_type, key=key)

    # Add target node to graph
    target_key = key if key_match else "diff_key"
    G.add_node("tgt_id", directive_type=dir_type, key=target_key)

    context = AddGraphEdgesContext(G=G)
    add_graph_edges = make_add_graph_edges(context)

    target_node = GraphNode(directive_type=dir_type, key=target_key, line_number=1, name="tgt_id")
    add_graph_edges(target_node)

    assert len(G.edges()) == expected_edges
    if expected_edges:
        assert G.has_edge("src_id", "tgt_id")