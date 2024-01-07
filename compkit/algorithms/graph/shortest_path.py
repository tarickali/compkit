"""
title : shortest_path.py
create : @tarickali 23/12/31
update : @tarickali 24/01/06
"""

from queue import Queue

from compkit.core import ID, Node, Number
from compkit.core.constants import Number, INF, DISTANCE, SPECIAL
from compkit.structures import Heap, Graph, DiGraph
from compkit.utils.types import create_links

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
        nodes to previous nodes in their shortest path from s

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

    Notes
    -----
    - This algorithm only computes the correct shortest pths in G if all
    edges in G have non-negative labels.

    Complexity
    ----------
    Space : O(n)
    Time : O((n + m)•log(n))

    """

    if s not in G:
        raise ValueError(f"Node={s} is not in G. Cannot compute shortest path.")

    s = s.uid if isinstance(s, Node) else s

    frontier: Heap = Heap(DISTANCE)
    explored: set[ID] | set[Node] = set()

    dist: dict[ID, Number] = {}
    if include_prev:
        prev: dict[ID, ID] = {}

    for x in G.get_nodes():
        dist[x] = INF
        if include_prev:
            prev[x] = None

    dist[s] = 0
    if include_prev:
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
                    if include_prev:
                        prev[y] = x
            else:
                dist[y] = temp
                if include_prev:
                    prev[y] = x
                frontier.insert(Node(y, {DISTANCE: temp}))

    if not include_prev:
        return dist
    else:
        return dist, prev


def bellman_ford(
    D: DiGraph, s: ID | Node, label: str, include_prev: bool = False
) -> dict[ID, Number] | tuple[dict[ID, Number], dict[ID, ID]] | None:
    """Compute the shortest path from s to every reachable node in D.

    Parameters
    ----------
    D : DiGraph
        The graph to compute shortest paths on from s
    s : ID | Node
        The start node for computing layers
    label : str
        The edge label to be used to compute shortest paths over
    include_prev : bool = False
        Determines if the function will return a dictionary mapping
        nodes to previous nodes in their shortest path from s

    Returns
    -------
    dist : dict[ID, Number]
        A dictionary mapping each node x in D to its shortest path value
        from s
    prev : dict[ID, ID] {this is only returned if include_prev = True}
        A dictionary mapping each node x in D to its previous node y in x's
        shortest path from s
    None
        If D has a negative cycle

    Raises
    ------
    ValueError
        If s is not in D
    KeyError
        If there is an edge e in D that does not have label in e.data

    Warnings
    --------
    - If e[label] maps to a non-Number object, then this function may have
    unexpected behavior. However, if e[label] has well-defined mathematical
    operations, then this function should behave as expected.

    Notes
    -----
    - This algorithm can compute the correct shortest paths in D even if the
    edge labels are negative numbers. However, this algorithm cannot compute
    the correct shortest path if D has neagtive cycles.

    Complexity
    ----------
    Space : O(n)
    Time : O(m•n)

    """

    if s not in D:
        raise ValueError(f"Node={s} is not in D. Cannot compute shortest path.")

    s = s.uid if isinstance(s, Node) else s

    dist: dict[ID, Number] = {}
    if include_prev:
        prev: dict[ID, ID] = {}

    for x in D.get_nodes():
        dist[x] = INF
        if include_prev:
            prev[x] = None

    dist[s] = 0
    if include_prev:
        prev[s] = None
    changed: bool = False

    for i in range(D.order):
        changed = False
        for e in D.get_edges(as_links=True):
            if dist.get(e.xid, INF) + e[label] < dist.get(e.yid, INF):
                dist[e.yid] = dist[e.xid] + e[label]
                if include_prev:
                    prev[e.yid] = e.xid
                changed = True
        if changed == False:
            break

    # Check if D has a negative cycle
    if changed == True and i == D.order - 1:
        return None

    if not include_prev:
        return dist
    else:
        return dist, prev


def floyd_warshall(
    D: DiGraph, label: str, include_succ: bool = False
) -> (
    dict[ID, dict[ID, Number]]
    | tuple[dict[ID, dict[ID, Number]], dict[ID, dict[ID, ID]]]
    | None
):
    """Compute the shortest path between every pair of nodes in D.

    Parameters
    ----------
    D : DiGraph
        The graph to compute shortest paths on from s
    label : str
        The edge label to be used to compute shortest paths over
    include_succ : bool = False
        Determines if the function will return a dictionary mapping
        nodes to successor nodes in their shortest paths

    Returns
    -------
    dist : dict[ID, dict[ID, Number]]
        A dictionary mapping each node y in D to its shortest path value
        from each node x in D
    succ : dict[ID, dict[ID, ID]]
        A dictionary mapping each node y in D to its successor node z in its
        shortest path from each node x in D
    None
        If D has a negative cycle

    Raises
    ------
    KeyError
        If there is an edge e in D that does not have label in e.data

    Warnings
    --------
    - If e[label] maps to a non-Number object, then this function may have
    unexpected behavior. However, if e[label] has well-defined mathematical
    operations, then this function should behave as expected.

    Notes
    -----
    - This algorithm can compute the correct shortest paths in D even if the
    edge labels are negative numbers. However, this algorithm cannot compute
    the correct shortest paths if D has negative cycles.

    Complexity
    ----------
    Space : O(n^2)
    Time : O(n^3)

    """

    dist: dict[ID, dict[ID, Number]] = {}
    if include_succ:
        succ: dict[ID, dict[ID, ID]] = {}

    nodes = D.get_nodes()
    for x in nodes:
        dist[x], succ[x] = {}, {}
        for y in nodes:
            dist[x][y] = INF
            if include_succ:
                succ[x][y] = None
        dist[x][x] = 0
        if include_succ:
            succ[x][x] = x

    for e in D.get_edges(as_links=True):
        # Skip self-loops
        if e.xid != e.yid:
            dist[e.xid][e.yid] = e[label]
            if include_succ:
                succ[e.xid][e.yid] = e.yid

    for z in nodes:
        for x in nodes:
            for y in D.nodes:
                if dist[x][y] > dist[x][z] + dist[z][y]:
                    dist[x][y] = dist[x][z] + dist[z][y]
                    if include_succ:
                        succ[x][y] = succ[x][z]

    for x in nodes:
        if dist[x][x] < 0:
            return None

    if not include_succ:
        return dist
    else:
        return dist, succ


def johnson(
    D: DiGraph, label: str, include_prev: bool = False
) -> (
    dict[ID, dict[ID, Number]]
    | tuple[dict[ID, dict[ID, Number]], dict[ID, dict[ID, ID]]]
    | None
):
    """Compute the shortest path between every pair of nodes in D.

    Parameters
    ----------
    D : DiGraph
        The graph to compute shortest paths on from s
    label : str
        The edge label to be used to compute shortest paths over
    include_prev : bool = False
        Determines if the function will return a dictionary mapping
        nodes to previous nodes in their shortest paths

    Returns
    -------
    dist : dict[ID, dict[ID, Number]]
        A dictionary mapping each node y in D to its shortest path value
        from each node x in D
    prev : dict[ID, dict[ID, ID]]
        A dictionary mapping each node y in D to its previous node z in its
        shortest path from each node x in D
    None
        If D has a negative cycle

    Raises
    ------
    KeyError
        If there is an edge e in D that does not have label in e.data

    Warnings
    --------
    - If e[label] maps to a non-Number object, then this function may have
    unexpected behavior. However, if e[label] has well-defined mathematical
    operations, then this function should behave as expected.

    - D must not contain a node with uid SPECIAL = "special"

    Notes
    -----
    - This algorithm can compute the correct shortest paths in D even if the
    edge labels are negative numbers. However, this algorithm cannot compute
    the correct shortest paths if D has negative cycles.

    Complexity
    ----------
    Space : O(m•n)
    Time : O((n + m)•n•log(n))

    """

    Dw = D.copy()

    temp = Node(SPECIAL)
    Dw.add_nodes(temp)
    Dw.add_edges(
        create_links(
            {(SPECIAL, yid): (temp.uid, yid, {label: 0}) for yid in Dw.get_nodes()}
        )
    )

    costs = bellman_ford(Dw, temp, label)

    if costs == None:
        return None

    for e in Dw.get_edges(as_links=True):
        Dw[e.xid, e.yid][label] = Dw[e.xid, e.yid][label] + costs[e.xid] - costs[e.yid]

    Dw.remove_node(temp)

    dist: dict[ID, dict[ID, Number]] = {}
    if include_prev:
        prev: dict[ID, dict[ID, ID]] = {}

    for x in D.get_nodes():
        if include_prev:
            dist[x], prev[x] = dijkstra(Dw, x, label, include_prev=include_prev)
        else:
            dist[x] = dijkstra(Dw, x, label, include_prev=include_prev)

    if not include_prev:
        return dist
    else:
        return dist, prev
