from src.syncspec.add_graph_edges_context import AddGraphEdgesContext
from src.syncspec.graph_node import GraphNode

def make_add_graph_edges(context: AddGraphEdgesContext):
    def add_graph_edges(node: GraphNode) -> None:
        source_type = None
        if node.directive_type == "include":
            source_type = "source"
        elif node.directive_type == "import":
            source_type = "export"
        else:
            return

        nodes = list(context.G.nodes(data=True))
        for node_id, attrs in nodes:
            if attrs.get('directive_type') == source_type and attrs.get('key') == node.key:
                context.G.add_edge(node_id, node.name)
    return add_graph_edges