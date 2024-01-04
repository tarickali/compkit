"""
title : minimum_cut.py
create : @tarickali 24/01/03
update : @tarickali 24/01/03
"""

import math

from compkit.core import ID, Node
from compkit.structures import Graph

from .connectivity import connected

__all__ = ["karger"]


def karger(G: Graph, T: int = None) -> tuple[tuple[set[ID], set[ID]], int]:
    """Compute a minimum cut of G.

    Parameters
    ----------
    G : Graph
        The graph to compute the minimum cut on
    T : int = None
        The number of iterations to execute the `mincut` subroutine (see Notes)

    Returns
    -------
    cut : tuple[set[ID], set[ID]]
        The minimum cut (A, B) of G, where A, B are sets of IDs of the nodes
        that are in each partition
    size : int
        The size of the minimum cut of G

    Raises
    ------
    ValueError
        If G is directed, G.order < 2, or G is not connected

    Notes
    -----
    - Karger's minimum cut algorithm is a randomized algorithm. As such, it is
    not guaranteed that the output of the algorithm is a minimum cut. The
    probability of outputting a true minimum cut of G increases as the number
    of iterations T of the subrountine increases. By default, T = nC2 * ln(n),
    which gives a probability of 1/n that the output is not a minimum cut.

    Complexity
    ----------
    Space : O(n + m)
    Time : O(T m) = O(n^2•m•log(n)) (by default)

    """

    mincut_errors()

    key = "multinode"

    def mincut() -> tuple[tuple[set[ID], set[ID]], int]:
        H = G.copy()
        while H.order > 2:
            e = H.choose_edge()
            H.contract_edge(e, key=key)

        x, y = H.nodes
        return (x.data[key], y.data[key]), H.size

    if T == None:
        T = math.ceil(math.comb(G.order, 2) * math.log(G.order))

    best_cut, best_size = mincut()
    for _ in range(T - 1):
        cut, size = mincut()
        if size < best_size:
            best_cut, best_size = cut, size

    return best_cut, best_size


def mincut_errors(G: Graph) -> None:
    if G.is_directed:
        raise ValueError(
            "Cannot run minimum cut algorithm on a DiGraph D. "
            "Consider calling D.to_undirected() first and pass in the "
            "underlying undirected Graph."
        )
    if not connected(G):
        raise ValueError(
            "Cannot run minimum cut algorithm on a Graph that is not connected."
        )
    if G.order < 2:
        raise ValueError(
            "Cannot run minimum cut algorithm on a Graph with less than two nodes."
        )
