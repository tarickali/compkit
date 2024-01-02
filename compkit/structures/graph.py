"""
title : graph.py
create : @tarickali 23/12/27
update : @tarickali 24/01/01
"""

from __future__ import annotations
import copy
import random
from collections import defaultdict

from compkit.core import ID, Node, Link


class Graph:
    """Base class for all graphs."""

    def __init__(self, nodes: list[Node] = None, edges: list[Link] = None) -> None:
        self.nodes: dict[ID, Node] = {}
        self.edges: dict[ID, Link] = {}
        self.graph: dict[ID, dict[ID, set[ID]]] = {}  # node -> node -> edges

        if nodes is not None:
            self.add_nodes(nodes)
        if edges is not None:
            self.add_edges(edges)

    def null(self) -> bool:
        """Check if G has no nodes.

        Returns
        -------
        bool

        """

        return self.order == 0

    def empty(self) -> bool:
        """Check if G has no edges.

        Returns
        -------
        bool

        """

        return self.size == 0

    def add_node(self, x: Node) -> None:
        """Add node x to G.

        If x is in G, then this method does nothing.

        Parameters
        ----------
        x : Node

        """

        if x.uid in self.nodes:
            return None

        self.nodes[x.uid] = x
        self.graph[x.uid] = defaultdict(set)

    def add_nodes(self, xs: list[Node]) -> None:
        """Add nodes xs to G.

        If a node x in xs is in G, then this method does nothing.

        Parameters
        ----------
        xs : list[Node]

        """

        for x in xs:
            self.add_node(x)

    def remove_node(self, x: ID | Node) -> None:
        """Remove node x and its incident edges from G.

        If x is not in G, then this method does nothing.

        Parameters
        ----------
        x : ID | Node

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            return None

        for yid in self.graph[xid]:
            eids = self.graph[yid].pop(xid)
            for eid in eids:
                self.edges.pop(eid)
        self.graph.pop(xid)

        self.nodes.pop(xid)

    def remove_nodes(self, xs: list[ID | Node]) -> None:
        """Remove nodes xs and their incident edges from G.

        If a node x in xs is not in G, then this method will ignore that node.

        Parameters
        ----------
        xs : list[ID | Node]

        """

        for x in xs:
            self.remove_node(x)

    def get_node(self, xid: ID) -> Node | None:
        """Get node G with ID xid.

        If no node with ID xid is in G, then this method does nothing.

        Parameters
        ----------
        xid : ID

        Returns
        -------
        Node | None

        """

        return self.nodes.get(xid)

    def get_nodes(self, as_nodes: bool = False) -> list[ID] | list[Node]:
        """Get all the nodes of G.

        Parameters
        ----------
        as_nodes : bool = False
            Determines if the return value is ID or Node

        Returns
        -------
        list[ID] | list[Node]
            If as_nodes = True, returns list[Node], otherwise returns an list[ID]

        """

        if as_nodes:
            return list(self.nodes.values())
        else:
            return list(self.nodes.keys())

    def choose_node(self, as_nodes: bool = False) -> ID | Node:
        """Randomly choose a node from G.

        Parameters
        ----------
        as_nodes : bool = False
            Determines if the return value is ID or Node

        Returns
        -------
        ID | Node
            If as_nodes = True, returns a Node, otherwise returns an ID

        Raises
        ------
        ValueError
            If G.order < 1

        """

        if self.order < 1:
            raise ValueError("Cannot sample one node from G as G.order is 0.")

        population = self.nodes.values() if as_nodes else self.nodes.keys()
        return random.choice(list(population))

    def sample_nodes(self, k: int = 1, as_nodes: bool = False) -> list[ID] | list[Node]:
        """Sample k random nodes from G.

        Parameters
        ----------
        k : int = 1
            The number of nodes to sample from G
        as_nodes : bool = False
            Determines if the return value is ID or Node

        Returns
        -------
        list[ID] | list[Node]
            If as_nodes = True, returns a Node, otherwise returns an ID

        Raises
        ------
        ValueError
            If k > G.order

        """

        if k > self.order:
            raise ValueError(
                f"G has {self.order} nodes, cannot sample {k} > {self.order} nodes."
            )

        population = self.nodes.values() if as_nodes else self.nodes.keys()
        return random.sample(list(population), k)

    def add_edge(self, e: Link) -> None:
        """Add edge e to G.

        For e = (x, y), if e is in G, then this method does nothing. If
        x or y are not in G, then this method will add new nodes to G,
        with uids x or y and without data.

        Parameters
        ----------
        e : Link

        """

        if e.uid in self.edges:
            return None

        self.add_nodes([Node(e.xid), Node(e.yid)])

        self.edges[e.uid] = e
        self.graph[e.xid][e.yid].add(e.uid)
        self.graph[e.yid][e.xid].add(e.uid)

    def add_edges(self, es: list[Link]) -> None:
        """Add edges es to G.

        If an edge e in es is in G, then this method does nothing.

        Parameters
        ----------
        es : list[Link]

        """

        for e in es:
            self.add_edge(e)

    def remove_edge(self, e: ID | Link) -> None:
        """Remove edge e from G.

        If e is not in G, then this method does nothing.

        Parameters
        ----------
        e : ID | Link

        """

        eid = e.uid if isinstance(e, Link) else e

        if eid not in self.edges:
            return None

        e = self.edges[eid]
        self.graph[e.xid][e.yid].remove(eid)
        self.graph[e.yid][e.xid].remove(eid)
        self.edges.pop(eid)

    def remove_edges(self, es: list[ID | Link]) -> None:
        """Remove edges es from G.

        If an edge e is not in G, then this method will ignore that edge.

        Parameters
        ----------
        e : ID | Link

        """

        for e in es:
            self.remove_edge(e)

    def get_edge(self, eid: ID) -> Link | None:
        """Get edge in G with ID eid.

        If no edge with ID eid is in G, then this method does nothing.

        Parameters
        ----------
        eid : ID

        Returns
        -------
        Link | None

        """

        return self.edges.get(eid)

    def get_edges(self, as_links: bool = False) -> list[ID] | list[Link]:
        """Get all the edges of G.

        Parameters
        ----------
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        list[ID] | list[Link]
            If as_links = True, returns list[Link], otherwise returns an list[ID]

        """

        if as_links:
            return list(self.edges.values())
        else:
            return list(self.edges.keys())

    def choose_edge(self, as_links: bool = False) -> ID | Link:
        """Randomly choose an edge from G.

        Parameters
        ----------
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        ID | Link
            If as_links = True, returns a Link, otherwise returns an ID

        Raises
        ------
        ValueError
            If G.size < 1

        """

        if self.size < 1:
            raise ValueError("Cannot sample one edge from G as G.size is 0.")

        population = self.edges.values() if as_links else self.edges.keys()
        return random.choice(list(population))

    def sample_edges(self, k: int = 1, as_links: bool = False) -> list[ID] | list[Link]:
        """Sample k random edges from G.

        Parameters
        ----------
        k : int = 1
            The number of edges to sample from G
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        list[ID] | list[Link]
            If as_links = True, returns a Link, otherwise returns an ID

        Raises
        ------
        ValueError
            If k > G.size

        """

        if k > self.size:
            raise ValueError(
                f"G has {self.size} edges, cannot sample {k} > {self.size} edges."
            )

        population = self.edges.values() if as_links else self.edges.keys()
        return random.sample(list(population), k)

    def get_edges_between(
        self, x: ID | Node, y: ID | Node, as_links: bool = False
    ) -> list[Link]:
        """Get the edges in G between nodes x and y.

        Parameters
        ----------
        x : ID | Node
        y : ID | Node
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        list[ID] | list[Link]
            If as_links = True, returns list[Link], otherwise returns list[ID]

        Raises
        ------
        KeyError
            If x or y are not in G

        """

        xid = x.uid if isinstance(x, Node) else x
        yid = y.uid if isinstance(y, Node) else y

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")
        if yid not in self.nodes:
            raise KeyError(f"Node with uid={yid} is not in G.")

        if as_links:
            return [self.edges[eid] for eid in self.graph[xid].get(yid, [])]
        else:
            return list(self.graph[xid].get(yid, []))

    def adjacent(self, x: ID | Node, as_nodes: bool = False) -> list[ID] | list[Node]:
        """Get the adjacent nodes of x in G.

        Parameters
        ----------
        x : ID | Node
        as_nodes : bool = False
            Determines if the return value is ID or Node

        Returns
        -------
        list[ID] | list[Node]
            If as_nodes = True, returns list[Node], otherwise returns list[ID]

        Raises
        ------
        KeyError
            If x is not in G

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        if as_nodes:
            return [self.nodes[yid] for yid in self.graph[xid]]
        else:
            return list(self.graph[xid])

    def incident(self, x: ID | Node, as_links: bool = False) -> list[ID] | list[Link]:
        """Get the incident edges of x in G.

        Parameters
        ----------
        x : ID | Node
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        list[ID] | list[Link]
            If as_links = True, returns list[Link], otherwise returns list[ID]

        Raises
        ------
        KeyError
            If x is not in G

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        if as_links:
            return [
                self.edges[eid]
                for eid in [eid for eids in self.graph[xid].values() for eid in eids]
            ]
        else:
            return [eid for eids in self.graph[xid].values() for eid in eids]

    def neighbors(self, x: ID | Node, y: ID | Node) -> bool:
        """Check if y is a neighbor of x in G.

        A node y is a neighbor of a node x in G if the edge (x, y) is in G,
        or equivalently, if y is in G.adjacent(x).

        If either x or y is not in G, then this method returns False.

        Parameters
        ----------
        x : ID | Node
        y : ID | Node

        Returns
        -------
        bool

        """

        xid = x.uid if isinstance(x, Node) else x
        yid = y.uid if isinstance(y, Node) else y

        if xid not in self.nodes or yid not in self.nodes:
            return False
        return yid in self.graph[xid]

    def degree(self, x: ID | Node) -> int:
        """Get the number of incident edges of x in G.

        Parameters
        ----------
        x : ID | Node

        Returns
        -------
        int

        Raises
        ------
        KeyError
            If x is not in G

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        return len(self.graph[xid])

    def contract_edge(self, e: ID | Link, key: str = "multinode") -> None:
        """Contract an edge e in G.

        For e = (x, y), if e is not in G, then this method does nothing.

        Parameters
        ----------
        e : ID | Link
        key : str = "multinode"

        Note
        ----
        This method will keep the left node x of e in G and will remove the
        right node y of e from G.

        This method will modify the data of x by adding x.data[key],
        which stores the IDs of all nodes of the original graph that
        have been contracted into x. If key is already in x.data, then
        this method will either add y to x.data[key] or merge y.data[key]
        with x.data[key].

        Warning
        -------
        To use this method without issues, ensure that the key provided is
        uniquely used for this method.

        """

        eid = e.uid if isinstance(e, Link) else e

        if eid not in self.edges:
            return None

        xid = self.edges[eid].xid
        yid = self.edges[eid].yid

        multinode_xids = self.nodes[xid].get(key, {xid})
        multinode_yids = self.nodes[yid].get(key, {yid})
        self.nodes[xid][key] = multinode_xids | multinode_yids

        self.remove_edge(eid)

        for zid in self.adjacent(yid):
            edges = self.get_edges_between(yid, zid)
            self.remove_edges(edges)
            self.add_edges([Link(f.uid, xid, zid, f.data) for f in edges])

        self.remove_node(yid)

    def get_loops(self, as_links: bool = False) -> list[ID] | list[Link]:
        """Get all loops in G.

        A loop in G is an edge e = (x, y) such that x == y.

        Parameters
        ----------
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        list[ID] | list[Link]
            If as_links = True, returns a Link, otherwise returns an ID

        """

        loops = []
        for eid, e in self.edges.items():
            if e.xid == e.yid:
                if as_links:
                    loops.append(e)
                else:
                    loops.append(eid)
        return loops

    def has_loops(self) -> bool:
        """Determine if G has any loops.

        A loop in G is an edge e = (x, y) such that x == y.

        Returns
        -------
        bool

        """

        return len(self.get_loops()) != 0

    def remove_loops(self) -> None:
        """Remove all loops in G.

        A loop in G is an edge e = (x, y) such that x == y.

        """

        loops = self.get_loops()
        self.remove_edges(loops)

    def has_parallel_edges(self) -> bool:
        """Determine if G has any parallel edges.

        Returns
        -------
        bool

        """

        for xid in self.nodes:
            for yid in self.adjacent(yid):
                if len(self.get_edges_between(xid, yid)) > 1:
                    return True
        return False

    def is_simple(self) -> bool:
        """Determine if G is a simple graph.

        A simple graph is one that does not have any loops or parallel edges.

        Returns
        -------
        bool

        """

        return not self.has_loops() and not self.has_parallel_edges()

    def copy(self) -> Graph:
        """Create a deepcopy of G.

        Returns
        -------
        Graph

        """

        return copy.deepcopy(self)

    def clear(self) -> None:
        """Remove all nodes and edges from G."""

        self.nodes.clear()
        self.edges.clear()
        self.graph.clear()

    def to_undirected(self) -> Graph:
        """Get the undirected graph of G.

        Returns
        -------
        G : Graph

        Note
        ----
        If G is an undirected graph then this method will return a shallow
        copy of G. Otherwise for nodes x, y with edges (x, y) and (y, x) in D,
        there will be a pair of parallel edges between x, y in G and all edge
        IDs will remain the same.

        """

        return self

    def to_directed(self) -> DiGraph:
        """Get the directed graph of G.

        Returns
        -------
        D : DiGraph

        Note
        ----
        If G is a directed graph then this method will return a shallow of G.
        Otherwise, for each edge e in the undirected graph G their IDs in D
        will be (0, e.uid) and (1, e.uid) for the forward and reverse edges in
        D, respectively, but e.data will be the same on both edges.

        """

        D = DiGraph()
        for e in self.edges:
            D.add_edge(Link((0, e.uid), e.xid, e.yid, e.data))
            D.add_edge(Link((1, e.uid), e.yid, e.xid, e.data))
        return D

    @property
    def order(self) -> int:
        """Number of nodes in G.

        Returns
        -------
        int

        """

        return len(self.nodes)

    @property
    def size(self) -> int:
        """Number of edges in G.

        Returns
        -------
        int

        """

        return len(self.edges)

    @property
    def is_undirected(self) -> bool:
        """Whether G is undirected or not.

        Returns
        -------
        bool

        """

        return True

    @property
    def is_directed(self) -> bool:
        """Whether G is directed or not.

        Returns
        -------
        bool

        """

        return False

    def __getitem__(self, uids: ID | tuple[ID, ID]) -> Node | list[Link]:
        """Get the node or list of edges in G of the given uid(s).

        If one ID is given, then this method will return the node
        associated with that ID in G.

        If two IDs are given, then this method will return the list of
        edges between the corresponding nodes in G

        Parameters
        ----------
        uids : ID | tuple[ID, ID]

        Returns
        -------
        Node | list[Link]

        Raises
        ------
        KeyError
            If a given ID is not in G
        KeyError
            If more than two IDs are passed into this method

        """

        if not isinstance(uids, tuple):
            uids = tuple([uids])

        if len(uids) > 2:
            raise KeyError(
                f"Cannot index into a Graph with more than two IDs and "
                f"{len(uids)} IDs were passed."
            )
        elif len(uids) == 2:
            xid, yid = uids
            return self.get_edges_between(xid, yid)
        else:  # == 1:
            (xid,) = uids
            return self.get_node(xid)

    def __contains__(self, x: ID | Node) -> bool:
        """Check if x is a node in G.

        Parameters
        ----------
        x : ID | Node

        Returns
        -------
        bool

        """

        xid = x.uid if isinstance(x, Node) else x

        return xid in self.nodes

    def __str__(self) -> str:
        """A description of the nodes and edges of G.

        Returns
        -------
        str

        """

        return f"Graph(nodes={self.nodes}, edges={self.edges})"


class DiGraph(Graph):
    """Base class for digraphs."""

    def __init__(self, nodes: list[Node] = None, edges: list[Link] = None) -> None:
        self.nodes: dict[ID, Node] = {}
        self.edges: dict[ID, Link] = {}
        self.forwardG: dict[ID, dict[ID, set[ID]]] = {}  # node -> node -> edges
        self.reverseG: dict[ID, dict[ID, set[ID]]] = {}  # node -> node -> edges

        if nodes is not None:
            self.add_nodes(nodes)
        if edges is not None:
            self.add_edges(edges)

    def add_node(self, x: Node) -> None:
        if x.uid in self.nodes:
            return None

        self.nodes[x.uid] = x
        self.forwardG[x.uid] = defaultdict(set)
        self.reverseG[x.uid] = defaultdict(set)

    def remove_node(self, x: ID | Node) -> None:
        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            return None

        for yid in self.forwardG[xid]:
            eids = self.reverseG[yid].pop(xid)
            for eid in eids:
                self.edges.pop(eid)
        self.forwardG.pop(xid)

        for yid in self.reverseG[xid]:
            eids = self.forwardG[yid].pop(xid)
            for eid in eids:
                self.edges.pop(eid)
        self.reverseG.pop(xid)

        self.nodes.pop(xid)

    def add_edge(self, e: Link) -> None:
        if e.uid in self.edges:
            return None

        self.add_nodes([Node(e.xid), Node(e.yid)])

        self.edges[e.uid] = e
        self.forwardG[e.xid][e.yid].add(e.uid)
        self.reverseG[e.yid][e.xid].add(e.uid)

    def remove_edge(self, e: ID | Link) -> None:
        eid = e.uid if isinstance(e, Link) else e

        if eid not in self.edges:
            return None

        e = self.edges[eid]

        self.forwardG[e.xid][e.yid].remove(eid)
        self.reverseG[e.yid][e.xid].remove(eid)
        self.edges.pop(eid)

    def get_edges_between(
        self, x: ID | Node, y: ID | Node, as_links: bool = False
    ) -> list[Link]:
        xid = x.uid if isinstance(x, Node) else x
        yid = y.uid if isinstance(y, Node) else y

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")
        if yid not in self.nodes:
            raise KeyError(f"Node with uid={yid} is not in G.")

        if as_links:
            return [self.edges[eid] for eid in self.forwardG[xid].get(yid, [])]
        else:
            return list(self.forwardG[xid].get(yid, []))

    def adjacent(self, x: ID | Node, as_nodes: bool = False) -> list[ID] | list[Node]:
        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        if as_nodes:
            return [self.nodes[yid] for yid in self.forwardG[xid]]
        else:
            return list(self.forwardG[xid])

    def coadjacent(
        self, x: ID | Node, as_nodes: bool = False
    ) -> list[ID] | list[Node] | None:
        """Get the coadjacent nodes of x in G.

        A coadjacent node of x in G is a node y such that there is
        an edge (y, x) in G.

        Parameters
        ----------
        x : ID | Node
        as_nodes : bool = False
            Determines if the return value is ID or Node

        Returns
        -------
        list[ID] | list[Node]
            If as_nodes = True, returns list[Node], otherwise returns list[ID]

        Raises
        ------
        KeyError
            If x is not in G

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        if as_nodes:
            return [self.nodes[yid] for yid in self.reverseG[xid]]
        else:
            return list(self.reverseG[xid])

    def incident(self, x: ID | Node, as_links: bool = False) -> list[ID] | list[Link]:
        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        if as_links:
            return [
                self.edges[eid]
                for eid in [eid for eids in self.forwardG[xid].values() for eid in eids]
            ]
        else:
            return [eid for eids in self.forwardG[xid].values() for eid in eids]

    def coincident(self, x: ID | Node, as_links: bool = False) -> list[ID] | list[Link]:
        """Get the coincident edges of x in G.

        A coincident edge of x in G is an edge e such that e = (y, x)
        where y is any node in G.

        Parameters
        ----------
        x : ID | Node
        as_links : bool = False
            Determines if the return value is ID or Link

        Returns
        -------
        list[ID] | list[Link]
            If as_links = True, returns list[Link], otherwise returns list[ID]

        Raises
        ------
        KeyError
            If x is not in G

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        if as_links:
            return [
                self.edges[eid]
                for eid in [eid for eids in self.reverseG[xid].values() for eid in eids]
            ]
        else:
            return [eid for eids in self.reverseG[xid].values() for eid in eids]

    def neighbors(self, x: ID | Node, y: ID | Node) -> bool:
        xid = x.uid if isinstance(x, Node) else x
        yid = y.uid if isinstance(y, Node) else y

        if xid not in self.nodes or yid not in self.nodes:
            return False
        return yid in self.forwardG[xid]

    def coneighbors(self, x: ID | Node, y: ID | Node) -> bool:
        """Check if y is a neighbor of x in G.

        A node y is a coneighbor of a node x in G if the edge (y, x) is in G,
        or equivalently, if x is in G.adjacent(y).

        If either x or y is not in G, then this method returns False.

        Parameters
        ----------
        x : ID | Node
        y : ID | Node

        Returns
        -------
        bool

        """

        xid = x.uid if isinstance(x, Node) else x
        yid = y.uid if isinstance(y, Node) else y

        if xid not in self.nodes or yid not in self.nodes:
            return False
        return yid in self.reverseG[xid]

    def degree(self, x: ID | Node) -> int:
        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        return sum([len(es) for es in self.forwardG[xid].values()])

    def codegree(self, x: ID | Node) -> int:
        """Get the number of coincident edges of x in G.

        Parameters
        ----------
        x : ID | Node

        Returns
        -------
        int

        Raises
        ------
        KeyError
            If x is not in G

        """

        xid = x.uid if isinstance(x, Node) else x

        if xid not in self.nodes:
            raise KeyError(f"Node with uid={xid} is not in G.")

        return sum([len(es) for es in self.reverseG[xid].values()])

    def copy(self) -> DiGraph:
        """Returns a copy of D.

        Returns
        -------
        DiGraph

        """

        return super().copy()

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()
        self.forwardG.clear()
        self.reverseG.clear()

    def transpose(self, inplace: bool = True) -> DiGraph:
        """Reverse the edges of D.

        Parameters
        ----------
        inplace : bool = True
            Determines if the edges of D are reversed inplace or not

        Returns
        -------
        DiGraph
            If inplace = True, returns a shallow copy of D, otherwise returns
            a deepcopy of D

        """

        D = self if inplace else self.copy()

        for e in D.get_edges(as_links=True):
            D.edges[e.uid] = Link(e.uid, e.yid, e.xid, e.data)
        D.forwardG, D.reverseG = D.reverseG, D.forwardG

        return D

    def to_undirected(self) -> Graph:
        G = Graph()
        for e in self.edges:
            G.add_edge(e)
        return G

    def to_directed(self) -> DiGraph:
        return self

    @property
    def is_undirected(self) -> bool:
        return False

    @property
    def is_directed(self) -> bool:
        return True
