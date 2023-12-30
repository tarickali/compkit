"""
title : union_find.py
create : @tarickali 23/12/28
update : @tarickali 23/12/29
"""

from typing import Any
from dataclasses import dataclass

from compkit.core import ID, Node


@dataclass
class Data:
    parent: ID = None
    rank: int = 0


class UnionFind:
    """Generic union-find data structure.

    Notation
    --------
    U : the union-find data structure

    Implementation Note
    -------------------
    This data structure is implemented with union-by-rank and path splitting.
    As such on an instance with |U|=n items and |O|=m U.find and U.union
    operations, the amortized time complexity is O(m•α(n)), i.e. each operation
    has amortize cost of O(α(n)).

    """

    def __init__(self) -> None:
        self.items: dict[ID, Node]
        self.datum: dict[ID, Data] = {}

    def add(self, item: Node) -> None:
        """Add and create a new partition for item in U.

        If item is in U, then this method does nothing.

        Parameters
        ----------
        item : Node

        """

        if item.uid in self.items:
            return None

        self.items[item.uid] = item
        self.datum[item.uid] = Data()

    def find(self, item: ID | Node) -> ID | None:
        """Find the representation ID of the partition of item in U.

        If item is not in U, then this method will return None.

        Parameters
        ----------
        item : ID | Node

        Returns
        -------
        ID | None

        """

        uid = item.uid if isinstance(item, Node) else item

        if uid not in self.items:
            return None

        cid = uid
        while self.datum[cid].parent != None:
            parent = self.datum[cid].parent
            grandparent = self.datum[parent].parent
            cid, self.datum[cid].parent = parent, grandparent
        return cid

    def union(self, u: ID | Node, v: ID | Node) -> None:
        """Merge the partitions of u and v into one partition in U.

        Parameters
        ----------
        u : ID | Node
        v : ID | Node

        """

        uid = u.uid if isinstance(u, Node) else u
        vid = v.uid if isinstance(v, Node) else v

        uset = self.find(uid)
        vset = self.find(vid)

        if uset == None or vset == None:
            return None

        if uset == vset:
            return None

        if self.datum[uset].rank < self.datum[vset].rank:
            uset, vset = vset, uset

        self.datum[vset].parent = uset
        if self.datum[uset].rank == self.datum[vset].rank:
            self.datum[uset].rank += 1

    def get_item(self, uid: ID) -> Node | None:
        """Get item in G with ID uid.

        Parameters
        ----------
        uid : ID

        Returns
        -------
        Node | None

        """

        return self.items.get(uid)

    @property
    def size(self) -> int:
        """Get the number of items in U.

        Returns
        -------
        int

        """

        return len(self.items)

    def __len__(self) -> int:
        """Get the number of items in U.

        Returns
        -------
        int

        """

        return len(self.items)

    def __getitem__(self, uid: ID) -> Node | None:
        """Get item in G with ID uid.

        Parameters
        ----------
        uid : ID

        Returns
        -------
        Node | None

        """

        return self.get_node(uid)
