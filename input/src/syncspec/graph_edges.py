from typing import Callable
from src.syncspec.edge import Edge
from src.syncspec.graph_edges_context import GraphEdgesContext


def make_graph_edges(context: GraphEdgesContext) -> Callable[[Edge], None]:
    def graph_edges(edge: Edge) -> None:
        target_id = f"{edge.directive_type}_{edge.name}_{edge.line_number}"
        source_map = {"include": "source", "import": "export"}
        source_type = source_map.get(edge.directive_type)

        if not source_type:
            return

        nodes = list(context.G.nodes(data=True))
        for node_id, attrs in nodes:
            if attrs.get("directive_type") == source_type and attrs.get("key") == edge.key:
                context.G.add_edge(node_id, target_id)

    return graph_edges