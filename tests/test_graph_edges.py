import pytest
import networkx as nx
from src.syncspec.edge import Edge
from src.syncspec.graph_edges_context import GraphEdgesContext
from src.syncspec.graph_edges import make_graph_edges


@pytest.mark.parametrize("dtype, key, sources, expected_count", [
    ("include", "libA", [("source_libA_1", "libA")], 1),
    ("import", "modB", [("export_modB_2", "modB")], 1),
    ("include", "libC", [("source_libD_3", "libD")], 0),
])
def test_graph_edges(dtype, key, sources, expected_count):
    G = nx.DiGraph()
    for nid, skey in sources:
        G.add_node(nid, directive_type=nid.split("_")[0], key=skey, name="n", line_number=1)

    target_id = f"{dtype}_main_10"
    G.add_node(target_id, directive_type=dtype, key=key, name="main", line_number=10)

    ctx = GraphEdgesContext(G=G)
    make_graph_edges(ctx)(Edge(dtype, key, 10, "main"))

    assert len(ctx.G.edges()) == expected_count