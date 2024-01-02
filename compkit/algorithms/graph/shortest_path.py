"""
title : shortest_path.py
create : @tarickali 23/12/31
update : @tarickali 24/01/01
"""

from queue import Queue

from compkit.core import ID, Node, Number
from compkit.core.constants import Number, INF, DISTANCE
from compkit.structures import Graph, Heap

__all__ = [
    "graph_layers",
    "dijkstra",
]


def graph_layers(G: Graph, s: ID | Node) -> dict[ID, int]:
    """Compute the layer for all reachable nodes from s.

    The layer of a node x from s is the minimum number of edges
    to traverse to reach x from s.

    Note that if x is not reachable from s in G, then layers[x] = INF.

    Parameters
    ----------
    G : Graph
        The graph to compute layers of from s
    s : ID | Node
        The start node for computing layers

    Returns
    -------
    dict[ID, int]
        A dictionary mapping node IDs to their layer number from s

    Raises
    ------
    ValueError
        If s is not in G

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    """

    if s not in G:
        raise ValueError(f"Node={s} is not in G. Cannot compute graph layers.")

    layers: dict[ID, int] = {x: INF for x in G.get_nodes()}
    queue: Queue[ID] = Queue()

    layers[s] = 0
    queue.put(s)

    while not queue.empty():
        x = queue.get()
        for y in G.adjacent(x):
            if layers[y] == INF:
                layers[y] = layers[x] + 1
                queue.put(y)

    return layers


def dijkstra(
    G: Graph, s: ID | Node, label: str, include_prev: bool = False
) -> dict[ID, Number] | tuple[dict[ID, Number], dict[ID, ID]]:
    """Compute the shortest path from s to every reachable node in G.

    This algorithm only computes the correct shortest pths in G if all
    edges in G have non-negative labels.

    Parameters
    ----------
    G : Graph
        The graph to compute shortest paths on from s
    s : ID | Node
        The start node for computing layers
    label : str
        The edge label to be used to compute shortest paths over
    include_prev : bool = False
        Determines if the function will return a dictionary mapping
        nodes to previous nodes in the shortest path from s

    Returns
    -------
    dist : dict[ID, Number]
        A dictionary mapping each node x in G to its shortest path value
        from s
    prev : dict[ID, ID] {this is only returned if include_prev = True}
        A dictionary mapping each node x in G to its previous node y in x's
        shortest path from s

    Raises
    ------
    ValueError
        If s is not in G
    KeyError
        If there is an edge e in G that does not have label in e.data

    Warnings
    --------
    - If G has an edge e such that the label on e is negative then this method
    is not guaranteed to return the correct shortest paths.

    - If e[label] maps to a non-Number object, then this function may have
    unexpected behavior. However, if e[label] has well-defined mathematical
    operations, then this function should behave as expected.

    Complexity
    ----------
    Space : O(n)
    Time : O((n + m) log n)

    """

    if s not in G:
        raise ValueError(f"Node={s} is not in G. Cannot compute shortest path.")

    s = s.uid if isinstance(s, Node) else s

    frontier: Heap = Heap(DISTANCE)
    explored: set[ID] | set[Node] = set()

    dist: dict[ID, Number] = {}
    prev: dict[ID, ID] = {}

    for x in G.get_nodes():
        dist[x] = INF
        prev[x] = None

    dist[s] = 0
    prev[s] = None
    frontier.insert(Node(s, {DISTANCE: 0}))

    while not frontier.empty():
        x = frontier.extract()
        explored.add(x)
        dist[x.uid] = x[DISTANCE]

        for y in G.adjacent(x):
            if y in explored:
                continue

            best = min(e[label] for e in G.get_edges_between(x, y))
            temp = dist[x] + best

            if y in frontier:
                if temp < frontier[y][DISTANCE]:
                    frontier.modify(y, {DISTANCE: temp})
                    prev[y] = x
            else:
                dist[y] = temp
                prev[y] = x
                frontier.insert(Node(y, {DISTANCE: temp}))

    if not include_prev:
        return dist
    else:
        return dist, prev
