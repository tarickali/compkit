"""
title : traversal.py
create : @tarickali 23/12/30
update : @tarickali 23/12/31
"""

from typing import Literal
from queue import Queue

from compkit.core import ID, Node
from compkit.structures import Graph

__all__ = [
    "breadth_first_search",
    "depth_first_search",
    "graph_search",
]


def breadth_first_search(
    G: Graph, s: ID | Node, ignore: set[ID] | set[Node] = None, as_nodes: bool = False
) -> set[ID]:
    """Breadth-first search on G from start node s.

    The frontier of explored nodes in G is expanded by exploring
    the neighboring nodes of fronter nodes.

    This method will find all reachable nodes in G from s, in turn
    it will return the connected component of s in G.

    Parameters
    ----------
    G : Graph
        The graph to traverse
    s : ID | Node
        The node to start the traversal from
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored
    as_nodes : bool = False
        Determines if the return value is ID or Node

    Returns
    -------
    set[ID] | set[Node]
        If as_nodes = True, returns set[Node], otherwise returns set[ID]

    Raises
    ------
    KeyError
        If s is not in G

    Warnings
    --------
    - The elements of ignore should have the same type as s, otherwise
    unexpected behaviors may arise due to set hashing in Python. Therefore if
    type(s) = ID then ensure type(ignore) = set[ID] or if type(s) = Node then
    ensure type(ignore) = set[Node].

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    depth_first_search : depth-first search
    graph_search : complete graph traversal

    """

    if s not in G:
        raise KeyError(
            f"{s} is not in G. Cannot traverse G from a node not in the graph."
        )

    if ignore is None:
        ignore = set()

    explored: set[ID] | set[Node] = set()
    queue: Queue[ID] | Queue[Node] = Queue()

    explored.add(s)
    queue.put(s)

    while not queue.empty():
        x = queue.get()
        for y in G.adjacent(x, as_nodes=as_nodes):
            if y not in explored and y not in ignore:
                explored.add(y)
                queue.put(y)

    return explored


def depth_first_search(
    G: Graph,
    s: ID | Node,
    ignore: set[ID] | set[Node] = None,
    as_nodes: bool = False,
    recursive: bool = False,
) -> set[ID]:
    """Depth-first search on G from start node s.

    The frontier of explored nodes in G is expanded by exploring
    full-depth paths from nodes.

    This method will find all reachable nodes in G from s, in turn
    it will return the connected component of s in G.

    Parameters
    ----------
    G : Graph
        The graph to traverse
    s : ID | Node
        The node to start the traversal from
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored
    as_nodes : bool = False
        Determines if the return value is ID or Node
    recursive : bool = False
        Determines if the traversal should be performed recursively or
        iteratively

    Returns
    -------
    set[ID] | set[Node]
        If as_nodes = True, returns set[Node], otherwise returns set[ID]

    Raises
    ------
    KeyError
        If s is not in G

    Warnings
    --------
    - The elements of ignore should have the same type as s, otherwise
    unexpected behaviors may arise due to set hashing in Python. Therefore if
    type(s) = ID then ensure type(ignore) = set[ID] or if type(s) = Node then
    ensure type(ignore) = set[Node].

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    breadth_first_search : breadth-first search
    graph_search : complete graph traversal

    """

    if s not in G:
        raise KeyError(
            f"{s} is not in G. Cannot traverse G from a node not in the graph."
        )

    if ignore is None:
        ignore = set()

    explored: set[ID] | set[Node] = set()

    explored.add(s)

    def recursion(x: ID | Node) -> None:
        explored.add(x)
        for y in G.adjacent(x, as_nodes=as_nodes):
            if y not in explored and y not in ignore:
                recursion(y)

    def iteration() -> None:
        stack: list[ID] | list[Node] = []

        explored.add(s)
        stack.append(s)

        while len(stack) != 0:
            x = stack.pop()
            for y in G.adjacent(x, as_nodes=as_nodes):
                if y not in explored and y not in ignore:
                    explored.add(y)
                    stack.append(y)

    if recursive:
        recursion(s)
    else:
        iteration()

    return explored


def graph_search(
    G: Graph,
    traversal_method: Literal["bfs", "dfs"] = "bfs",
    ignore: set[ID] | set[Node] = None,
    as_nodes: bool = False,
) -> list[set[ID]] | list[set[Node]]:
    """Perform a complete search of G, traversing all nodes.

    Parameters
    ----------
    G : Graph
        The graph to traverse
    traversal_method : Literal["bfs", "dfs"] = "bfs"
        The method to traverse G by
    ignore : set[ID] | set[Node] = None
        A set of nodes to ignore when traversing G, typically nodes that
        were already explored
    as_nodes : bool = False
        Determines if the return value is ID or Node

    Returns
    -------
    list[set[ID]] | list[set[Node]]
        A list all connected components in G. If as_nodes = True, returns
        list[set[Node]], otherwise returns list[set[ID]]

    Raises
    ------
    ValueError
        If traversal_method is not "bfs" or "dfs"

    Warnings
    --------
    - The elements of ignore should have the same type as s, otherwise
    unexpected behaviors may arise due to set hashing in Python. Therefore if
    type(s) = ID then ensure type(ignore) = set[ID] or if type(s) = Node then
    ensure type(ignore) = set[Node].

    - The usage of this function is only well-defined for undirected graphs.
    It can be run on directed graphs, however the output of this function
    depends on the order of nodes visited and hence has unexpected behavior.
    For a well-defined search function for directed graphs, refer to
    stronly_connected_components.

    Complexity
    ----------
    Space : O(n)
    Time : O(n + m)

    See Also
    --------
    bfs : breadth-first search
    dfs : depth-first search
    connected_components : (weakly) connected components of graphs
    strongly_connected_components : connected components of digraphs

    """

    explored: set[ID] | set[Node] = set()
    components: list[set[ID]] | list[set[Node]] = []

    traverse = None
    if traversal_method == "bfs":
        traverse = breadth_first_search
    elif traversal_method == "dfs":
        traverse = depth_first_search
    else:
        raise ValueError(f"Traversal method {traversal_method} is not supported.")

    # NOTE: do not need to update ignore or pass explored due to bfs/dfs guarantees
    for x in G.get_nodes(as_nodes=as_nodes):
        if x not in explored and x not in ignore:
            component = traverse(G, x, ignore=ignore, as_nodes=as_nodes)
            explored |= component
            components.append(component)

    return components
