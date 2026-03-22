import pytest
import importlib.util
import os

def load_module():
    spec = importlib.util.spec_from_file_location("syncspec_graph", "src/syncspec/syncspec-graph.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

syncspec = load_module()
process_graph = syncspec.process_graph
parse_dot_file = syncspec.parse_dot_file

def _wrap(content):
    return f"strict digraph {{ {content} }}"

@pytest.mark.parametrize("content, error", [
    ("strict graph {}", "Input must be a digraph"),
    (_wrap("a->b;"), "must not contain edges"),
    (_wrap('"n" [directive_type=export];'), "missing string attribute"),
    (_wrap('"n" [directive_type=export, key="k", file_name="f", line_number="x"];'), "line_number must be integer"),
])
def test_validation(tmp_path, content, error):
    p = tmp_path / "in.dot"
    p.write_text(content)
    with pytest.raises(ValueError, match=error):
        process_graph(str(p))

def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        process_graph(str(tmp_path / "missing.dot"))

@pytest.mark.parametrize("dtype, key, target_type, has_edge", [
    ("include", "k", "source", True),
    ("include", "k", "export", False),
    ("import", "k", "export", True),
    ("import", "k", "source", False),
])
def test_edges(tmp_path, dtype, key, target_type, has_edge):
    p = tmp_path / "in.dot"
    n1 = f'"from_node" [directive_type={target_type}, key="{key}", line_number=1, file_name="f"];'
    n2 = f'"to_node" [directive_type={dtype}, key="{key}", line_number=2, file_name="f"];'
    p.write_text(_wrap(f"{n1} {n2}"))
    process_graph(str(p))
    G = parse_dot_file(str(p))
    assert G.has_edge("from_node", "to_node") == has_edge

@pytest.mark.parametrize("dtype, expected_color", [
    ("include", "yellow"),
    ("import", "red"),
])
def test_edge_color(tmp_path, dtype, expected_color):
    p = tmp_path / "in.dot"
    if dtype == "include":
        n1 = '"from_node" [directive_type=source, key="k", line_number=1, file_name="f"];'
    else:
        n1 = '"from_node" [directive_type=export, key="k", line_number=1, file_name="f"];'
    n2 = f'"to_node" [directive_type={dtype}, key="k", line_number=2, file_name="f"];'
    p.write_text(_wrap(f"{n1} {n2}"))
    process_graph(str(p))
    content = p.read_text()
    assert f'color={expected_color}' in content

def test_edge_directive_type(tmp_path):
    p = tmp_path / "in.dot"
    n1 = '"from_node" [directive_type=export, key="k", line_number=1, file_name="f"];'
    n2 = '"to_node" [directive_type=import, key="k", line_number=2, file_name="f"];'
    p.write_text(_wrap(f"{n1} {n2}"))
    process_graph(str(p))
    content = p.read_text()
    assert 'directive_type=import' in content

def test_node_decoration(tmp_path):
    p = tmp_path / "in.dot"
    p.write_text(_wrap('"n" [directive_type=export, key="k", line_number=5, file_name="f"];'))
    process_graph(str(p))
    content = p.read_text()
    assert 'fillcolor=lightblue' in content
    assert 'shape=circle' in content
    assert 'label="5"' in content

@pytest.mark.parametrize("dtype, expected_color", [
    ("export", "lightblue"),
    ("source", "lightblue"),
    ("import", "lightgreen"),
    ("include", "lightgreen"),
])
def test_node_colors(tmp_path, dtype, expected_color):
    p = tmp_path / "in.dot"
    p.write_text(_wrap(f'"n" [directive_type={dtype}, key="k", line_number=1, file_name="f"];'))
    process_graph(str(p))
    content = p.read_text()
    assert f'fillcolor={expected_color}' in content

def test_grouping(tmp_path):
    p = tmp_path / "in.dot"
    p.write_text(_wrap('"n" [directive_type=export, key="k", line_number=1, file_name="myfile"];'))
    process_graph(str(p))
    content = p.read_text()
    assert 'subgraph cluster_myfile' in content

def test_output_path(tmp_path):
    inp = tmp_path / "in.dot"
    out = tmp_path / "out.dot"
    inp.write_text(_wrap('"n" [directive_type=export, key="k", line_number=1, file_name="f"];'))
    process_graph(str(inp), str(out))
    assert out.exists()
    assert inp.exists()

def test_edge_label(tmp_path):
    p = tmp_path / "in.dot"
    n1 = '"from_node" [directive_type=export, key="mykey", line_number=1, file_name="f"];'
    n2 = '"to_node" [directive_type=import, key="mykey", line_number=2, file_name="f"];'
    p.write_text(_wrap(f"{n1} {n2}"))
    process_graph(str(p))
    G = parse_dot_file(str(p))
    data = G.get_edge_data("from_node", "to_node")
    assert data is not None
    assert data.get('label') == 'mykey'