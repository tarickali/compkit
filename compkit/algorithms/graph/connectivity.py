"""
title : connectivity.py
create : @tarickali 23/12/30
update : @tarickali 23/12/31
"""

from compkit.core import ID, Node
from compkit.structures import Graph, DiGraph

from .traversal import graph_search

__all__ = [
    "connected_components",
    "connectivity",
    "connected",
    "strongly_connected_components",
    "strong_connectivity",
    "strongly_connected",
]


def connected_components(
    G: Graph, ignore: set[ID] | set[Node] = None, as_nodes: bool = False
) -> list[set[ID]] | list[set[Node]]:
    """Find all the connected components of G.

    Parameters
    ----------
    G : Graph
        The graph to find the connected components of
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored
    as_nodes : bool = False
        Determines if the return value is ID or Node

    Returns
    -------
    list[set[ID]] | list[set[Node]]
        A list of the weakly connected components in G. If as_nodes = True,
        returns list[set[Node]], otherwise returns list[set[ID]]

    Warnings
    --------
    - The elements of ignore should have the same type as the expected return
    type of the function, otherwise unexpected behaviors may arise due to set
    hashing in Python. In particular, if as_nodes = False then ensure
    type(ignore) = set[ID] or if as_nodes = True then ensure type(ignore) = set[Node].

    Notes
    -----
    - If G is a directed graph, this function will return the weakly connected
    components of G. Specifically, it will find the connected components of the
    underlying undirected graph of G. For the strongly connected components of
    a directed graph, refer to strongly_connected_components.

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    strongly_connected_components : connected components of digraphs

    """

    T = G.to_undirected()
    return graph_search(T, traversal_method="bfs", ignore=ignore, as_nodes=as_nodes)


def connectivity(G: Graph, ignore: set[ID] | set[Node] = None) -> int:
    """Determine the number of connected components of G.

    Parameters
    ----------
    G : Graph
        The graph to determine the connectivity of
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored

    Returns
    -------
    int
        The number of connected components of G

    Notes
    -----
    - If G is a directed graph, this function will only determine the connectivity
    of the underlying undirected graph of G. For the connectivity of the digraph G,
    refer to strongly_connected_components.

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    connected_components : (weakly) connected components of graphs
    strong_connectivity : connectivity for digraphs

    """

    as_nodes = False
    if ignore is not None and len(ignore) != 0:
        i = ignore.pop()
        as_nodes = isinstance(i, Node)
        ignore.add(i)

    return len(connected_components(G, ignore=ignore, as_nodes=as_nodes))


def connected(G: Graph, ignore: set[ID] | set[Node] = None) -> bool:
    """Determine if G is connected.

    Parameters
    ----------
    G : Graph
        The graph to determine if it is connected or not
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored

    Returns
    -------
    bool
        True if and only if G is weakly connected

    Notes
    -----
    - If G is a directed graph, this function will only determine if G is weakly
    connected, i.e. that the underlying undirected graph is connected. To determine
    if the digraph G is connected, refer to strongly_connected.

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    connectivity : number of (weakly) connected components of graphs
    strongly_connected : determine if digraphs are connected

    """

    return connectivity(G, ignore=ignore) <= 1


def strongly_connected_components(
    D: DiGraph, ignore: set[ID] | set[Node] = None, as_nodes: bool = False
) -> list[set[ID]] | list[set[Node]]:
    """Find all the strongly connected components of D.

    Parameters
    ----------
    D : DiGraph
        The digraph to find the connected components of
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored
    as_nodes : bool = False
        Determines if the return value is ID or Node

    Returns
    -------
    list[set[ID]] | list[set[Node]]
        A list of the strongly connected components in G. If as_nodes = True,
        returns list[set[Node]], otherwise returns list[set[ID]]

    Warnings
    --------
    - The elements of ignore should have the same type as the expected return
    type of the function, otherwise unexpected behaviors may arise due to set
    hashing in Python. In particular, if as_nodes = False then ensure
    type(ignore) = set[ID] or if as_nodes = True then ensure type(ignore) = set[Node].

    Implementation Note
    -------------------
    This function implements Kosaraju's two-pass algorithm to find the strongly
    connected components of G.

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    connected_components : (weakly) connected components of graphs

    """

    explored: set[ID] | set[Node] = set()
    ordering: list[ID] | set[Node] = []
    assigned: dict[ID, int] | dict[Node, int] = {}

    def visit(x: ID | Node) -> None:
        explored.add(x)
        for y in D.coadjacent(x, as_nodes=as_nodes):
            if y not in explored and y not in ignore:
                visit(y)
        ordering.append(x)

    def assign(x: ID | Node, c: int) -> None:
        assigned[x] = c
        for y in D.adjacent(x, as_nodes=as_nodes):
            if y not in assigned and y not in ignore:
                assigned(y, c)

    for x in D.get_nodes(as_nodes=as_nodes):
        if x not in explored and x not in ignore:
            visit(x)

    c = 0
    for x in reversed(ordering):
        if x not in assigned and x not in ignore:
            assign(x, c)
            c += 1

    components: list[set[ID]] | list[set[Node]] = [set() for _ in range(c)]
    for x, c in assigned.items():
        components[c].add(x)

    return components


def strong_connectivity(D: DiGraph, ignore: set[ID] | set[Node] = None) -> int:
    """Determine the number of strongly connected components of D.

    Parameters
    ----------
    D : DiGraph
        The digraph to determine the connectivity of
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored

    Returns
    -------
    int
        The number of strongly connected components of D

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    strongly_connected_components : strongly connected components of digraphs
    connectivity : connectivity for graphs

    """

    as_nodes = False
    if ignore is not None and len(ignore) != 0:
        i = ignore.pop()
        as_nodes = isinstance(i, Node)
        ignore.add(i)

    return len(strongly_connected_components(D, ignore=ignore, as_nodes=as_nodes))


def strongly_connected(D: DiGraph, ignore: set[ID] | set[Node] = None) -> bool:
    """Determine if D is strongly connected.

    Parameters
    ----------
    D : DiGraph
        The graph to determine if it is strongly connected or not
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored

    Returns
    -------
    bool
        True if and only if G is strongly connected

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    strong_connectivity : number of strongly connected components of digraphs
    connected : determine if graphs are connected

    """

    return strong_connectivity(D, ignore=ignore) <= 1
