"""
title : graphs.py
create : @tarickali 23/12/30
update : @tarickali 23/12/31
"""

import random
import itertools

from compkit.structures import Graph, DiGraph

from .types import create_nodes, create_links

__all__ = [
    "cycle_graph",
    "path_graph",
    "complete_graph",
    "random_graph",
    "complete_bipartite_graph",
    "random_bipartite_graph",
    "peterson_graph",
]


def cycle_graph(
    n: int, directed: bool = False, reverse: bool = False
) -> Graph | DiGraph:
    """Create the cycle graph C with n nodes.

    Parameters
    ----------
    n : int
        The number of nodes in C
    directed : bool = False
        Determines if C is directed or not
    reverse : bool = False
        Determines if the edges of C are reversed if it is directed

    Returns
    -------
    Graph | DiGraph
        If directed = False, returns Graph, otherwise returns DiGraph

    Raises
    ------
    ValueError
        If n <= 2

    """

    if n <= 2:
        raise ValueError(f"Cannot create a cycle graph with {n}<=2 nodes.")

    nodes = create_nodes(range(n))

    if not directed:
        edges = create_links(
            [(i, i, i + 1) for i in range(n - 1)] + [(n - 1, n - 1, 0)]
        )
        return Graph(nodes, edges)
    else:
        if not reverse:
            edges = create_links(
                [(i, i, i + 1) for i in range(n - 1)] + [(n - 1, n - 1, 0)]
            )
            return DiGraph(nodes, edges)
        else:
            edges = create_links(
                [(i, i + 1, i) for i in range(n - 1)] + [(n - 1, 0, n - 1)]
            )
            return DiGraph(nodes, edges)


def path_graph(
    n: int, directed: bool = False, reverse: bool = False
) -> Graph | DiGraph:
    """Create the path graph P with n nodes.

    Parameters
    ----------
    n : int
        The number of nodes in P
    directed : bool = False
        Determines if P is directed or not
    reverse : bool = False
        Determines if the edges of P are reversed if it is directed

    Returns
    -------
    Graph | DiGraph
        If directed = False, returns Graph, otherwise returns DiGraph

    Raises
    ------
    ValueError
        If n <= 1

    """

    if n <= 1:
        raise ValueError(f"Cannot create a path graph with {n}<=1 nodes.")

    nodes = create_nodes(range(n))

    if not directed:
        edges = create_links([(i, i, i + 1) for i in range(n - 1)])
        return Graph(nodes, edges)
    else:
        if not reverse:
            edges = create_links([(i, i, i + 1) for i in range(n - 1)])
            return DiGraph(nodes, edges)
        else:
            edges = create_links([(i, i + 1, i) for i in range(n - 1)])
            return DiGraph(nodes, edges)


def complete_graph(n: int) -> Graph:
    """Create the complete graph K with n nodes.

    Parameters
    ----------
    n : int
        The number of nodes in K

    Returns
    -------
    Graph

    Raises
    ------
    ValueError
        If n <= 0

    """

    if n <= 0:
        raise ValueError(f"Cannot create a complete with {n}<=0 nodes.")

    nodes = create_nodes(range(n))

    edges = []
    e = 0
    for x in range(n):
        for y in range(x + 1, n):
            edges.append((e, x, y))
            e += 1
    edges = create_links(edges)

    return Graph(nodes, edges)


def random_graph(n: int, size: int, directed: bool = False) -> Graph | DiGraph:
    """Create a random graph R with n nodes.

    Parameters
    ----------
    n : int
        The number of nodes in R
    size : int
        The number of random edges in R
    directed : bool = False
        Determines if R is directed or not

    Returns
    -------
    Graph | DiGraph
        If directed = False, returns Graph, otherwise returns DiGraph

    Raises
    ------
    ValueError
        If n <= 0
    ValueError
        If size > n * (n-1) / 2 when directed = False or size > n * (n - 1) when
        directed = True

    Note
    ----
    This function will always return a simple graph, one with not loop and
    parallel edges.

    """

    if n <= 0:
        raise ValueError(f"Cannot create a random graph with {n}<=0 nodes.")
    if not directed and size > n * (n - 1) // 2:
        raise ValueError(
            f"Cannot create a random graph with {n} nodes and {size} edges."
        )
    if directed and size > n * (n - 1):
        raise ValueError(
            f"Cannot create a random digraph with {n} nodes and {size} edges."
        )

    nodes = create_nodes(range(n))

    if not directed:
        population = list(itertools.combinations(range(n), 2))
    else:
        population = list(itertools.permutations(range(n), 2))

    edges = random.sample(population, size)
    edges = create_links([(e, x, y) for e, (x, y) in enumerate(edges)])

    if not directed:
        return Graph(nodes, edges)
    else:
        return DiGraph(nodes, edges)


def complete_bipartite_graph(n: int, m: int) -> Graph:
    """Create the complete bipartite graph B with n + m nodes.

    Parameters
    ----------
    n : int
        The number of nodes in the left partition of B
    m : int
        The number of nodes in the right partition of B

    Returns
    -------
    Graph

    Raises
    ------
    ValueError
        If n <= 0 or m <= 0

    """

    if n <= 0 or m <= 0:
        raise ValueError(
            f"Cannot create a bipartite graph with {n}<=0 and {m}<=0 nodes."
        )

    A = create_nodes(range(n))
    B = create_nodes(range(n, n + m))

    edges = create_links([(i * m + j, i, j + n) for i in range(n) for j in range(m)])

    return Graph(A + B, edges)


def random_bipartite_graph(n: int, m: int, size: int) -> Graph:
    """Create a random bipartite graph B with n + m nodes.

    Parameters
    ----------
    n : int
        The number of nodes in the left partition of B
    m : int
        The number of nodes in the right partition of B
    size : int
        The number of random edges in B

    Returns
    -------
    Graph

    Raises
    ------
    ValueError
        If n <= 0 or m <= 0
    ValueError
        If size > n*m

    """

    if n <= 0 or m <= 0:
        raise ValueError(
            f"Cannot create a bipartite graph with {n}<=0 and {m}<=0 nodes."
        )
    if size > n * m:
        raise ValueError(
            f"Cannot create a bipartite graph with {n * m} nodes and {size} edges."
        )

    A = create_nodes(range(n))
    B = create_nodes(range(n, n + m))

    population = list(itertools.product(range(n), range(n, n + m)))

    edges = random.sample(population, size)
    edges = create_links([(e, x, y) for e, (x, y) in enumerate(edges)])

    return Graph(A + B, edges)


def peterson_graph() -> Graph:
    """Create the Peterson graph K.

    Returns
    -------
    Graph

    """

    nodes = create_nodes(range(10))
    edges = create_links(
        [(i, i, i + 1) for i in range(4)]
        + [(4, 4, 0)]
        + [(i, i - 5, i) for i in range(5, 10)]
        + [(10, 5, 7), (11, 5, 8), (12, 6, 8), (13, 6, 9), (14, 7, 9)]
    )

    return Graph(nodes, edges)
