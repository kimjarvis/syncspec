from src.syncspec.node import Node
from src.syncspec.edge import Edge
from src.syncspec.combine_nodes_context import CombineNodesContext


def make_combine_nodes(context: CombineNodesContext):
    def combine_nodes(node: Node) -> Edge:
        dtype = node.directive_type
        node_id = f"{dtype}_{node.name}_{node.line_number}"
        label = f"{dtype}\n{node.name}\n:{node.line_number}"
        colors = {"source": "lightblue", "export": "red", "include": "lightgreen", "import": "yellow"}

        context.G.add_node(
            node_id, key=node.key, directive_type=dtype, label=label,
            shape="rectangle", style="filled", fillcolor=colors.get(dtype, "white")
        )
        return Edge(dtype, node.key, node.line_number, node.name)

    return combine_nodes
