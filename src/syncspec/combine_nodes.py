from src.syncspec.node import Node
from src.syncspec.combine_nodes_context import CombineNodesContext


def make_combine_nodes(context: CombineNodesContext):
    def combine_nodes(node: Node) -> None:
        node_id = f"{node.name}_{node.line_number}"

        if node.directive_type == "source":
            context.G.add_node(
                node_id,
                key=node.key,
                directive_type=node.directive_type,
                label=f"{node.name}\n{node.line_number}",
                shape="box",
                style="filled",
                fillcolor="lightblue"
            )

        elif node.directive_type == "include":
            matches = [
                nid for nid, attrs in context.G.nodes(data=True)
                if attrs.get("key") == node.key and attrs.get("directive_type") == "source"
            ]
            context.G.add_node(
                node_id,
                key=node.key,
                directive_type=node.directive_type,
                label=f"{node.name}\n{node.line_number}",
                shape="box",
                style="filled",
                fillcolor="lightgreen"
            )
            for src_id in matches:
                context.G.add_edge(src_id, node_id, label=node.key)

    return combine_nodes