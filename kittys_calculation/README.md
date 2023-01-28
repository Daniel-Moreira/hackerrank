# Kittys Calculation 
Kitty has a tree, , consisting of  nodes where each node is uniquely labeled from  to . Her friend Alex gave her  sets, where each set contains  distinct nodes. Kitty needs to calculate the following expression on each set:
$$\sum_{u,v} u * v * dist(u, v)$$
where:
${u,v}$ denotes an unordered pair of nodes belonging to the set.
$dist(u, v)$ denotes the number of edges on the unique (shortest) path between nodes $u$ and $v$.

## Optimization
To optimize this problem it is necessary to take several steps. First we start by analyzing the relation of the equation in function of its lowest common ancestor (LCA): 
$$\sum_{u,v} u * v * dist(u, v) = \sum_u \sum_v u * v [dist(u, L) + dist(L, v)]$$, where $L$ is the lowest common ancestor (LCA) between $u$ and $v$. Assuming $dist(u, L)$ takes $\mathcal{O}(1)$ then the whole computation takes $\mathcal{O}(u * v)$.
This resulting equation can be simplify further:
$$\sum_u \sum_v u * v [dist(u, L) + dist(L, v)] = \sum_u \sum_v u * v * dist(u, L) + \sum_u \sum_v u * v * dist(L, v)$$
$$\sum_u \sum_v u * v * dist(u, L) = \sum_u u * dist(u, L) \sum_v v$$
$$\sum_u \sum_v u * v * dist(L, v) = \sum_v v * dist(L, v) \sum_u u$$
Given $\sum_u u$ and $\sum_v v$ precomputed in $\mathcal{O}(1)$ the whole computation should take $2*\mathcal{O}(u + v)$.


For the first groups of nodes $g$ closer to the leafs we have the following base case with LCA $L^1$:
$$pre_1^1 = \sum_{u \in g} u * dist(u, L^1)$$
$$pre_2^1 = \sum_{u \in g} u$$
$$\sum_{u,v \in g} u * v * dist(u, v) = \sum_{u \in g} u * dist(u, L^1) * (pre_2^1 - u)$$

For the remaining groups of nodes we can calculate the kittys calculation based on $pre_1$ and $pre_2$ for $L^i$:
$$pre_1^i = \sum [pre_1^{i-1} + dist(L^{i-1}, L^{i}) * pre_2^{i-1}]$$
$$pre_2^i = \sum pre_2^{i-1}$$
$$\sum_{u,v} u * v * dist(u, v) = \sum [pre_1^{i-1} + dist(L^{i-1}, L^{i}) * pre_2^{i-1}] * (pre_2^{i} - pre_2^{i-1})$$
Note that for each group of node we have different values for $i$, $L^{i-1}$, $pre_1^{i-1}$ and $pre_2^{i-1}$.
