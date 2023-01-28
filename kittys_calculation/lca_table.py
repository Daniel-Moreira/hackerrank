class Node:
    value: int
    children: list["Node"]
    visited: bool
    distance: int

    def __init__(self, value: int) -> None:
        self.value = value
        self.children = []
        self.visited = False
        self.distance = 0


def lca(node: Node, lca_table: list[list[Node]]) -> set[Node]:
    node_set: set[Node] = {node}

    node.visited = True
    children_sets: list[set[Node]] = []
    for child in node.children:
        if not child.visited:
            child_set = lca(child, lca_table)
            node_set = node_set.union(child_set)
            children_sets.append(child_set)

    # Set lca between itself and each node in a child subtree to be itself
    for child in node_set:
        lca_table[node.value][child.value] = node
        lca_table[child.value][node.value] = node

    # Set lca between child subsets to be itself
    for i in range(len(children_sets)):
        set_u = children_sets[i]
        for j in range(i + 1, len(children_sets)):
            set_v = children_sets[j]
            for u in set_u:
                for v in set_v:
                    lca_table[u.value][v.value] = node
                    lca_table[v.value][u.value] = node

    return node_set


def calculate_distance(node: Node) -> None:
    queue: list[Node] = [node]

    while len(queue) > 0:
        u = queue.pop(0)

        u.visited = False
        for child in u.children:
            if child.visited:
                queue.append(child)
                child.distance = u.distance + 1


def get_distance(u: Node, v: Node, lca_table: list[list[Node]]) -> int:
    return u.distance + v.distance - 2 * lca_table[u.value][v.value].distance


def main():
    amount_nodes, amount_queries = input().strip().split(" ")
    amount_nodes = int(amount_nodes)
    amount_queries = int(amount_queries)

    nodes = [Node(i) for i in range(amount_nodes)]

    for _ in range(amount_nodes - 1):
        u, v = input().strip().split(" ")
        u = nodes[int(u) - 1]
        v = nodes[int(v) - 1]

        u.children.append(v)
        v.children.append(u)

    root = nodes[0]
    lca_table = [[None for _ in range(amount_nodes)] for _ in range(amount_nodes)]
    lca(root, lca_table)
    calculate_distance(root)

    for _ in range(amount_queries):
        amount_nodes = int(input().strip())
        query = []
        while len(query) < amount_nodes:
            query += [int(n) - 1 for n in input().strip().split(" ")]
        if len(query) == 1:
            query.append(query[0])

        kitty_calculation = 0
        for i in range(len(query)):
            for j in range(i + 1, len(query)):
                kitty_calculation += (
                    (query[i] + 1)
                    * (query[j] + 1)
                    * get_distance(nodes[query[i]], nodes[query[j]], lca_table)
                )
        print(kitty_calculation % (10**9 + 7))


if __name__ == "__main__":
    main()
