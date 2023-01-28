class Node:
    value: int
    children: list["Node"]
    distance: int

    def __init__(self, value: int) -> None:
        self.value = value
        self.children = []
        self.distance = 0


class PreprocessNode:
    distance: int
    sum_distance: int
    nodes_sum: int

    def __init__(self, distance: int, sum_distance: int, nodes_sum: int) -> None:
        self.distance = distance
        self.sum_distance = sum_distance
        self.nodes_sum = nodes_sum


def dfs(u: Node) -> list[Node]:
    stack: list[tuple[Node, Node]] = [(u, None)]
    node_order: list[Node] = []

    v: Node = None
    while len(stack) > 0:
        u, v = stack.pop()

        node_order.append(u)

        if v:
            u.distance = v.distance + 1
            u.children.remove(v)

        for child in u.children:
            stack.append((child, u))

    return node_order


def kitty_calculation(nodes_order: list[Node], query: set[Node]) -> int:
    nodes_processed: dict[Node, list[PreprocessNode]] = {}
    kitty_sum = 0

    for lca in reversed(nodes_order):
        children_set = set(lca.children)
        children_set.add(lca)
        query_childs = children_set.intersection(query)
        query = query.difference(children_set)

        if len(query_childs) == 0:
            continue

        nodes_sum = 0
        distance_sum = 0

        u_nodes: list[PreprocessNode] = []
        for u in query_childs:
            # Transform Node into a PreprocessNode
            if u not in nodes_processed:
                u_nodes.append(PreprocessNode(u.distance, 0, u.value))
            # Get the PreprocessNode
            else:
                u_nodes += nodes_processed[u]

        if len(u_nodes) == 1:
            if len(query) == 0:
                break

            query.add(lca)
            nodes_processed[lca] = u_nodes
            continue

        for u in u_nodes:
            nodes_sum += u.nodes_sum
            distance_sum += u.sum_distance + u.nodes_sum * (u.distance - lca.distance)

        for u in u_nodes:
            v_sum = nodes_sum - u.nodes_sum
            kitty_sum += (
                (
                    (u.nodes_sum * (u.distance - lca.distance)) % (10**9 + 7)
                    + u.sum_distance
                )
                % (10**9 + 7)
                * v_sum
            )

        kitty_sum = kitty_sum % (10**9 + 7)
        nodes_processed[lca] = [
            PreprocessNode(lca.distance, distance_sum % (10**9 + 7), nodes_sum)
        ]

        if len(query) == 0:
            break

        query.add(lca)

    return kitty_sum


def main():
    amount_nodes, amount_queries = input().split()
    amount_nodes = int(amount_nodes)
    amount_queries = int(amount_queries)

    nodes = [Node(i) for i in range(1, amount_nodes + 1)]

    for _ in range(amount_nodes - 1):
        u, v = input().split()
        u = nodes[int(u) - 1]
        v = nodes[int(v) - 1]

        u.children.append(v)
        v.children.append(u)

    root = nodes[0]
    nodes_order = dfs(root)

    for _ in range(amount_queries):
        input()
        query_set = {nodes[int(n) - 1] for n in input().split()}

        result = kitty_calculation(nodes_order, query_set)

        print(result)


if __name__ == "__main__":
    main()
