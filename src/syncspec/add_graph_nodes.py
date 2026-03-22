from src.syncspec.add_graph_nodes_context import AddGraphNodesContext
from src.syncspec.node import Node
from src.syncspec.graph_node import GraphNode


def make_add_graph_nodes(context: AddGraphNodesContext):
    def add_graph_nodes(node: Node) -> GraphNode:
        node_id = f"{node.directive_type}_{node.name}_{node.line_number}"
        context.G.add_node(
            node_id,
            directive_type=node.directive_type,
            key=node.key,
            line_number=node.line_number,
            file_name=node.name,
        )
        return GraphNode(
            directive_type=node.directive_type,
            key=node.key,
            line_number=node.line_number,
            name=node.name,
        )

    return add_graph_nodes