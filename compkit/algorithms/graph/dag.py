"""
title : dag.py
create : @tarickali 23/12/31
update : @tarickali 23/12/31
"""

from compkit.core import ID, Node
from compkit.structures import DiGraph

__all__ = [
    "is_cyclic",
    "is_acyclic",
    "topological_sort",
]


def is_cyclic(D: DiGraph) -> bool:
    """Determines if D is a directed cyclic graph.

    Parameters
    ----------
    D : DiGraph

    Returns
    -------
    bool

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    is_acyclic : determines if a digraph is a directed acyclic graph

    """

    explored: set[ID] = set()
    visited: set[ID] = set()

    def visit(x: ID) -> None:
        if x in visited:
            raise
        if x in explored:
            return

        visited.add(x)
        for y in D.adjacent(x):
            visit(y)

        visited.remove(x)
        explored.add(x)

    for x in D.get_nodes():
        if x not in explored:
            try:
                visit(x)
            except:
                return True

    return False


def is_acyclic(D: DiGraph) -> bool:
    """Determines if D is a directed acyclic graph.

    Parameters
    ----------
    D : DiGraph

    Returns
    -------
    bool

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    is_cyclic : determines if a digraph is a directed cyclic graph

    """

    return not is_cyclic(D)


def topological_sort(
    D: DiGraph, as_nodes: bool = False
) -> list[ID] | list[Node] | None:
    """Compute a topological ordering of D.

    A topological ordering of a digraph D is a linear ordering L of the nodes
    of D such that for every edge (x, y), x appears before y in L.

    Note that there exists at least one topological ordering of D if and only
    if D is a DAG (directed acyclic graph).

    If D is not a DAG, this function will return None.

    Parameters
    ----------
    D : DiGraph
        The digraph to find a topological order of
    as_nodes : bool = False
        Determines if the return value is ID or Node

    Returns
    -------
    ordering : list[ID] | list[Node]
        A topological ordering of D if it is a DAG. If as_nodes = True,
        returns set[Node], otherwise returns set[ID]
    None
        If D is not a DAG

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    """

    explored: set[ID] | set[Node] = set()
    visited: set[ID] | set[Node] = set()
    ordering: list[ID] | list[Node] = []

    def visit(x: ID | Node) -> None:
        if x in visited:
            raise
        if x in explored:
            return

        visited.add(x)
        for y in D.adjacent(x, as_nodes=as_nodes):
            visit(y)

        visited.remove(x)
        explored.add(x)
        ordering.append(x)

    for x in D.get_nodes(as_nodes=as_nodes):
        if x not in explored:
            try:
                visit(x)
            except:
                return None

    return ordering[::-1]
