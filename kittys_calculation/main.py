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
    nodes_order: list[Node], nodes_to_querys: list[set[int]]
) -> list[int]:
    nodes_processed_per_query: dict[Node, dict[int, list[PreprocessNode]]] = {
        u: { query: [PreprocessNode(u.distance, 0, u.value)] for query in nodes_to_querys[u.value] } for u in nodes_order
    }
    kitty_sums: dict[int, int] = defaultdict(int)

    for lca in reversed(nodes_order):
        # Get a map query -> list of found nodes around lca
        query_set: dict[int, list[PreprocessNode]] = defaultdict(list)
        for child in lca.children + [lca]:
            for i_query, nodes_processed in nodes_processed_per_query[child].items():
                query_set[i_query] += nodes_processed

        for i_query, u_nodes in query_set.items():
            nodes_sum = 0
            distance_sum = 0

            if len(u_nodes) == 1:
                continue

            for u in u_nodes:
                nodes_sum += u.nodes_sum
                distance_sum += u.sum_distance + (u.nodes_sum * (
                    u.distance - lca.distance
                )) % (10**9 + 7)

            kitty_sum = 0
            for u in u_nodes:
                v_sum = nodes_sum - u.nodes_sum
                kitty_sum += (
                    u.nodes_sum * (u.distance - lca.distance) + u.sum_distance
                ) * v_sum % (10**9 + 7)

            kitty_sums[i_query] = (kitty_sums[i_query] + kitty_sum) % (10**9 + 7)
            query_set[i_query] = [PreprocessNode(lca.distance, distance_sum, nodes_sum)]
        
        nodes_processed_per_query[lca] = query_set

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

    results = kitty_calculation(nodes_order, querys)

    for i in range(amount_queries):
        print(results[i])


if __name__ == "__main__":
    main()
