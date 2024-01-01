"""
title : shortest_path.py
create : @tarickali 23/12/31
update : @tarickali 23/12/31
"""

from queue import Queue

from compkit.core import ID, Node
from compkit.core.constants import INF
from compkit.structures import Graph

__all__ = ["graph_layers"]


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

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    """

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
