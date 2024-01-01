"""
title : bipartite.py
create : @tarickali 23/12/31
update : @tarickali 23/12/31
"""

from queue import Queue

from compkit.core import ID
from compkit.structures import Graph

__all__ = [
    "is_bipartite",
]


def is_bipartite(G: Graph) -> bool:
    """Checks if G is a bipartite graph.

    Parameters
    ----------
    G : Graph

    Returns
    -------
    bool

    Raises
    ------
    ValueError
        If G is a digraph or G.order < 2

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    """

    if G.is_directed:
        raise ValueError("G is a digraph, cannot check if G is bipartite.")
    if G.order < 2:
        raise ValueError("G.order < 2, cannot check if G is bipartite.")

    colors: dict[ID, int] = {}

    def coloring(s: ID) -> bool:
        queue: Queue[ID] = Queue()

        colors[s] = True
        queue.put(s)

        while not queue.empty():
            x = queue.get()
            for y in G.adjacent(x):
                if y in colors:
                    if colors[y] == colors[x]:
                        return False
                else:
                    colors[y] = not colors[x]
                    queue.put(y)

        return True

    for x in G.get_nodes():
        if x not in colors:
            valid = coloring(x)
            if not valid:
                return False
    return True
