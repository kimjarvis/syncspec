#!/usr/bin/env python3
import argparse
import sys
import os
import networkx as nx
import pydot


def _clean(val):
    """Strip quotes from pydot attribute values."""
    if isinstance(val, str):
        return val.strip('"')
    return val


def parse_dot_file(path):
    """Parse DOT file using pydot and return NetworkX DiGraph."""
    graphs = pydot.graph_from_dot_file(path)
    if not graphs:
        raise ValueError("Failed to parse DOT file")
    pd = graphs[0]

    if pd.get_graph_type() != 'digraph':
        raise ValueError("Input must be a digraph")

    G = nx.DiGraph()

    for node in pd.get_nodes():
        name = node.get_name()
        if name in ('node', 'edge', 'graph'):
            continue
        name = _clean(name)
        attrs = {k: _clean(v) for k, v in node.get_attributes().items()}
        G.add_node(name, **attrs)

    for edge in pd.get_edges():
        src = _clean(edge.get_source())
        dst = _clean(edge.get_destination())
        G.add_edge(src, dst)

    return G


def validate_graph(G):
    for name, attrs in G.nodes(data=True):
        for k in ['directive_type', 'file_name', 'key']:
            if k not in attrs:
                raise ValueError(f"Node {name} missing string attribute: {k}")
        if 'line_number' not in attrs:
            raise ValueError(f"Node {name} missing integer attribute: line_number")
        try:
            int(attrs['line_number'])
        except (ValueError, TypeError):
            raise ValueError(f"Node {name} line_number must be integer")


def add_edges(G):
    lookup = {}
    for n, d in G.nodes(data=True):
        lookup.setdefault((d['directive_type'], d['key']), []).append(n)

    for n, d in G.nodes(data=True):
        from_nodes = []
        if d['directive_type'] == 'include':
            from_nodes = lookup.get(('source', d['key']), [])
            edge_attrs = {'label': d['key'], 'directive_type': 'include', 'color': 'yellow'}
        elif d['directive_type'] == 'import':
            from_nodes = lookup.get(('export', d['key']), [])
            edge_attrs = {'label': d['key'], 'directive_type': 'import', 'color': 'red'}
        else:
            continue

        for from_node in from_nodes:
            G.add_edge(from_node, n, **edge_attrs)


def decorate(G):
    node_colors = {'export': 'lightblue', 'source': 'lightblue',
                   'import': 'lightgreen', 'include': 'lightgreen'}
    for n, d in G.nodes(data=True):
        d['shape'] = 'circle'
        d['style'] = 'filled'
        d['label'] = d['line_number']
        if d['directive_type'] in node_colors:
            d['fillcolor'] = node_colors[d['directive_type']]


def write_graph(G, output_path):
    pd = pydot.Dot(strict=True, graph_type='digraph')
    groups = {}

    for n, d in G.nodes(data=True):
        fname = d['file_name']
        if fname not in groups:
            sg = pydot.Subgraph(f"cluster_{fname}", label=fname)
            groups[fname] = sg
            pd.add_subgraph(sg)
        attrs = {k: str(v) for k, v in d.items()}
        groups[fname].add_node(pydot.Node(f'"{n}"', **attrs))

    for u, v, data in G.edges(data=True):
        edge_attrs = {}
        if 'label' in data:
            edge_attrs['label'] = data['label']
        if 'color' in data:
            edge_attrs['color'] = data['color']
        if 'directive_type' in data:
            edge_attrs['directive_type'] = data['directive_type']
        edge = pydot.Edge(f'"{u}"', f'"{v}"', **edge_attrs)
        pd.add_edge(edge)

    dot_string = pd.to_string()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(dot_string)


def process_graph(input_path, output_path=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path.endswith('.dot'):
        raise ValueError("Input file must have .dot suffix")
    if output_path and not output_path.endswith('.dot'):
        raise ValueError("Output file must have .dot suffix")

    G = parse_dot_file(input_path)

    if G.number_of_edges() > 0:
        raise ValueError("Input graph must not contain edges")

    validate_graph(G)
    add_edges(G)
    decorate(G)
    target = output_path if output_path else input_path
    write_graph(G, target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="Input .dot file")
    parser.add_argument('--output', help="Optional output .dot file")
    args = parser.parse_args()
    try:
        process_graph(args.path, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()