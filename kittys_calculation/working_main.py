from collections import defaultdict


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


def kitty_calculation(
    nodes_order: list[Node], nodes_to_querys: list[set[int]], amount_queries: int
) -> list[int]:
    nodes_processed_per_query: dict[int, dict[Node, list[PreprocessNode]]] = {
        i_query: {} for i_query in range(amount_queries)
    }
    kitty_sums: dict[int, int] = defaultdict(int)

    for lca in reversed(nodes_order):
        children_set = set(lca.children)
        children_set.add(lca)

        # Get a map query -> list of found nodes around lca
        query_set: dict[int, list[Node]] = defaultdict(list)
        for child in children_set:
            for u in nodes_to_querys[child.value]:
                query_set[u].append(child)
            nodes_to_querys[child.value] = set()

        for i_query, nodes in query_set.items():
            nodes_sum = 0
            distance_sum = 0

            nodes_processed = (
                nodes_processed_per_query[i_query]
                if i_query in nodes_processed_per_query
                else []
            )

            u_nodes: list[PreprocessNode] = []
            for u in nodes:
                # Transform Node into a PreprocessNode
                if u not in nodes_processed:
                    u_nodes.append(PreprocessNode(u.distance, 0, u.value))
                # Get the PreprocessNode
                else:
                    u_nodes += nodes_processed[u]

            if len(u_nodes) == 1:
                nodes_to_querys[lca.value].add(i_query)
                nodes_processed_per_query[i_query][lca] = u_nodes
                continue

            for u in u_nodes:
                nodes_sum += u.nodes_sum
                distance_sum += u.sum_distance + u.nodes_sum * (
                    u.distance - lca.distance
                ) % (10**9 + 7)

            for u in u_nodes:
                v_sum = nodes_sum - u.nodes_sum
                kitty_sums[i_query] += (
                    u.nodes_sum * (u.distance - lca.distance) + u.sum_distance
                ) * v_sum

            kitty_sums[i_query] = kitty_sums[i_query] % (10**9 + 7)
            nodes_processed_per_query[i_query].update(
                {lca: [PreprocessNode(lca.distance, distance_sum, nodes_sum)]}
            )

            nodes_to_querys[lca.value].add(i_query)

    return kitty_sums


def main():
    amount_nodes, amount_queries = input().strip().split()
    amount_nodes = int(amount_nodes)
    amount_queries = int(amount_queries)

    nodes = [Node(i) for i in range(1, amount_nodes + 1)]

    for _ in range(amount_nodes - 1):
        u, v = input().strip().split()
        u = nodes[int(u) - 1]
        v = nodes[int(v) - 1]

        u.children.append(v)
        v.children.append(u)

    querys: list[set[int]] = [set() for _ in range(amount_nodes + 1)]
    for i_query in range(amount_queries):
        input()
        for n in input().split():
            querys[int(n)].add(i_query)

    root = nodes[0]
    nodes_order = dfs(root)

    results = kitty_calculation(nodes_order, querys, amount_queries)

    for i in range(amount_queries):
        print(results[i])


if __name__ == "__main__":
    main()
