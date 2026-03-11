import pytest
import networkx as nx
from src.syncspec.node import Node
from src.syncspec.combine_nodes_context import CombineNodesContext
from src.syncspec.combine_nodes import make_combine_nodes


@pytest.mark.parametrize(
    "node, existing, exp_edges, exp_fillcolor",
    [
        (Node("source", "k1", 1, "A"), [], [], "lightblue"),
        (Node("include", "k1", 2, "B"), [], [], "lightgreen"),
        (Node("include", "k1", 2, "B"), [("A_1", {"key": "k1", "directive_type": "source"})],
         [("A_1", "B_2", {"label": "k1"})], "lightgreen"),
        (Node("include", "k1", 2, "B"), [("A_1", {"key": "k2", "directive_type": "source"})], [], "lightgreen"),
        (Node("include", "k1", 2, "B"), [("A_1", {"key": "k1", "directive_type": "include"})], [], "lightgreen"),
    ],
)
def test_combine_nodes(node, existing, exp_edges, exp_fillcolor):
    ctx = CombineNodesContext(G=nx.DiGraph())
    for nid, attrs in existing:
        ctx.G.add_node(nid, **attrs)

    fn = make_combine_nodes(ctx)
    fn(node)

    nid = f"{node.name}_{node.line_number}"
    assert nid in ctx.G.nodes
    assert ctx.G.nodes[nid]["fillcolor"] == exp_fillcolor
    assert ctx.G.nodes[nid]["shape"] == "box"
    assert ctx.G.nodes[nid]["key"] == node.key

    if exp_edges:
        for e in exp_edges:
            assert e in ctx.G.edges(data=True)
    else:
        assert len(ctx.G.edges()) == 0


def test_source_node_label():
    ctx = CombineNodesContext(G=nx.DiGraph())
    fn = make_combine_nodes(ctx)
    fn(Node("source", "k1", 10, "MyFile"))

    assert ctx.G.nodes["MyFile_10"]["label"] == "MyFile\n10"


def test_include_edge_label():
    ctx = CombineNodesContext(G=nx.DiGraph())
    ctx.G.add_node("A_1", key="mykey", directive_type="source",
                   label="A\n1", shape="box", style="filled", fillcolor="lightblue")
    fn = make_combine_nodes(ctx)
    fn(Node("include", "mykey", 2, "B"))

    edges = list(ctx.G.edges(data=True))
    assert len(edges) == 1
    assert edges[0][2]["label"] == "mykey"


def test_include_node_label():
    ctx = CombineNodesContext(G=nx.DiGraph())
    fn = make_combine_nodes(ctx)
    fn(Node("include", "k1", 5, "IncFile"))

    assert ctx.G.nodes["IncFile_5"]["label"] == "IncFile\n5"
    assert ctx.G.nodes["IncFile_5"]["fillcolor"] == "lightgreen"


def test_multiple_source_matches():
    ctx = CombineNodesContext(G=nx.DiGraph())
    ctx.G.add_node("A_1", key="shared", directive_type="source",
                   label="A\n1", shape="box", style="filled", fillcolor="lightblue")
    ctx.G.add_node("C_3", key="shared", directive_type="source",
                   label="C\n3", shape="box", style="filled", fillcolor="lightblue")
    fn = make_combine_nodes(ctx)
    fn(Node("include", "shared", 2, "B"))

    edges = list(ctx.G.edges(data=True))
    assert len(edges) == 2
    assert ("A_1", "B_2", {"label": "shared"}) in edges
    assert ("C_3", "B_2", {"label": "shared"}) in edges