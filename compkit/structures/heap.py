"""
title : heap.py
create : @tarickali 23/12/27
update : @tarickali 24/01/01
"""

from __future__ import annotations
from typing import Literal, Any

from compkit.core import ID, Node


class Heap:
    """Vanilla heap data structure.

    Items u, v in the heap will be compared based on the label parameter
    given at initialization. So, every item must have label in its data
    attribute. Also, u.data[label] must be a comparable type, such that
    <, =, > are defined for its data type.

    This data structure supports both min and max heaps, based on the mode
    parameter given at initialization.

    Notation
    --------
    H : the heap data structure.
    n : number of items in H.
    m : number of heaps in methods with multiple heaps.
    N : max number of items in a heap from a collection of multiple heaps.

    """

    def __init__(self, label: str, mode: Literal["min", "max"] = "min") -> None:
        self.label = label
        self.mode = mode

        self.items: list[Node] = []
        self.indices: dict[ID, int] = {}  # f : ID -> idx in self.items

    @staticmethod
    def heapify(
        items: list[Node], label: str, mode: Literal["min", "max"] = "min"
    ) -> Heap:
        """Create a {mode}-heap from a list of items.

        Parameters
        ----------
        items : list[Node]
        label : str
        mode : Literal['min', 'max'] = 'min'

        Returns
        -------
        Heap

        Complexity
        ----------
        Space : O(n)
        Time : O(n)

        """

        heap = Heap(label, mode)

        heap.items = [None] * len(items)
        for idx, item in enumerate(items):
            heap.items[idx] = item
            heap.indices[item.uid] = idx

        idx = heap._parent(heap.size() - 1)
        while idx >= 0:
            heap._bubble_down(idx)
            idx -= 1

        return heap

    @staticmethod
    def merge(
        heaps: list[Heap],
        label: str,
        mode: Literal["min", "max"] = "min",
        merged: bool = False,
    ) -> Heap:
        """Merge a collection of heaps into one {mode}-heap.

        Parameters
        ----------
        heaps : list[Heap]
        label : str
        mode : Literal['min', 'max'] = 'min'
        merged : bool = False

        Returns
        -------
        Heap

        Note
        ----
        To ensure uniqueness and avoid collisions of items in the
        new heap, we use the following scheme to construct the new
        ID of the Heap items.

        If merged=False (the heaps were not merged before), then the
        new ID is given by:
            new_uid = (old_uid, heap_idx).

        If merged=True (the heaps were merged before), then the new ID
        is given by:
            new_uid = (*old_uid, heap_idx).

        Therefore, the new ID for each item is given by:
            item.uid = (init_uid, i0, i1, i2, ...)
        where ik is the index of the kth heap container and init_uid is
        the item's original ID.

        As such to find the item's original ID after k merges one only needs
        to index the 0th index of merged item's ID.

        Furthermore, although the items in the new Heap are new Node objects
        with different IDs, they share the same data dictionary since a shallow
        copy is used to construct the new items.

        Complexity
        ----------
        Space : O(N•m)
        Time : O(N•m)

        """

        merged_items: list[Node] = []
        for i, heap in enumerate(heaps):
            for item in heap.items:
                if not merged:
                    merged_items.append(Node((item.uid, i), item.data))
                else:
                    merged_items.append(Node(item.uid + (i,), item.data))

        merged_heap = Heap.heapify(merged_items, label, mode)

        return merged_heap

    def root(self) -> Node | None:
        """Find the root item of H.

        If H is empty, then this method will return None.

        Returns
        -------
        Node | None

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        if self.size() == 0:
            return None
        return self.items[0]

    def insert(self, item: Node) -> None:
        """Inserts new item into H.

        If item.uid is in H, then this method will do nothing.

        Parameters
        ----------
        item : Node

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        if item.uid in self.indices:
            return None

        self.items.append(item)
        self.indices[item.uid] = self.size() - 1

        self._bubble_up(self.size() - 1)

    def extract(self) -> Node | None:
        """Delete and return root item of H.

        If root of H is None, then this method will return None.

        Returns
        -------
        Node | None

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        if self.size() == 0:
            return None

        root = self.root()
        self.delete(root)

        return root

    def get_item(self, uid: ID) -> Node | None:
        """Return item with ID uid from H.

        If nid is not in H, then this method will return None.

        Parameters
        ----------
        uid : ID

        Returns
        -------
        Node | None

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        item_idx = self.indices.get(uid)
        if item_idx == None:
            return None
        return self.items[item_idx]

    def replaceroot(self, item: Node) -> Node | None:
        """Replace root of H with item.

        If H is empty, then this method will do nothing and will
        return None. This ensures that the size invariant of H holds
        after this method is called.

        Parameters
        ----------
        item : Node

        Returns
        -------
        Node | None

        Note
        ----
        Using this method is more efficient than using separate calls to
        delete and insert.

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        if self.size() == 0:
            return None
        else:
            root = self.root()
            self.replace(self.items[0], item)
            return root

    def replace(self, old: ID | Node, new: Node) -> None:
        """Replace old item with a new item in H.

        If old is not in H, then this method does nothing.

        Parameters
        ----------
        old : ID | Node
        new : Node

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        oid = old.uid if isinstance(old, Node) else old

        old_idx = self.indices.get(oid)
        if old_idx == None:
            return None

        self.items[old_idx] = new
        self.indices.pop(oid)
        self.indices[new.uid] = old_idx

        # Note only one of the methods below will run, since invariant
        # changes in only one direction.
        self._bubble_up(old_idx)
        self._bubble_down(old_idx)

    def delete(self, item: ID | Node) -> None:
        """Delete item from H.

        If item is not in H, then this method will do nothing.

        Parameters
        ----------
        item : ID | Node

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        nid = item.uid if isinstance(item, Node) else item

        idx = self.indices.get(nid)
        if idx == None:
            return None

        self._swap(idx, self.size() - 1)
        self.items.pop()
        self.indices.pop(nid)

        # Note only one of the methods below will run, since invariant
        # changes in only one direction.
        self._bubble_up(idx)
        self._bubble_down(idx)

    def modify(self, uid: ID, data: dict[str, Any]) -> None:
        """Modify data of the item with the given ID.

        If no item with ID nid is in H, then this method does nothing.

        Parameters
        ----------
        uid : ID
        data : dict[str, Any]

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        self.replace(uid, Node(uid, data))

    def size(self) -> int:
        """Get the number of items in H.

        Returns
        -------
        int

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        return len(self.items)

    def empty(self) -> bool:
        """Check if H is empty.

        Returns
        -------
        bool

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        return self.size() == 0

    def clear(self) -> None:
        """Clears contents of H, in turn creating an empty heap.

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        self.items = []
        self.indices = {}

    def __getitem__(self, uid: ID) -> Node | None:
        """Return item with ID uid from H.

        If uid is not in H, then this method will return None.

        Parameters
        ----------
        uid : ID

        Returns
        -------
        Node | None

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        return self.get_item(uid)

    def __contains__(self, item: ID | Node) -> bool:
        """Checks if a item is in H.

        Parameters
        ----------
        item : ID | Node

        Returns
        -------
        bool

        """

        nid = item.uid if isinstance(item, Node) else item

        return nid in self.indices

    def __len__(self) -> int:
        """Get the number of items in H.

        Returns
        -------
        int

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        return self.size()

    def _parent(self, idx: int) -> int | None:
        """Get the parent index of idx in H.

        If idx is 0 (i.e. the root index), then this method returns None.

        Parameters
        ----------
        idx : int

        Returns
        -------
        int | None

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        if idx == 0:
            return None
        return (idx - 1) // 2

    def _left(self, idx: int) -> int | None:
        """Get the left child index of idx in H.

        If the given idx has no left child, then this method will return None.

        Parameters
        ----------
        idx : int

        Returns
        -------
        int | None

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        child = 2 * (idx + 1) - 1
        if child >= self.size():
            return None
        return child

    def _right(self, idx: int) -> int | None:
        """Get the right child index of idx in H.

        If the given idx has no right child, then this method will return None.

        Parameters
        ----------
        idx : int

        Returns
        -------
        int | None

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        child = 2 * (idx + 1)
        if child >= self.size():
            return None
        return child

    def _bubble_up(self, idx: int) -> None:
        """Restore invariant of H from idx by swapping items upwards.

        Parameters
        ----------
        idx : int

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        c = idx
        p = self._parent(idx)

        while p != None:
            if self._compare(self.items[c], self.items[p]):
                self._swap(c, p)
                c = p
                p = self._parent(c)
            else:
                break

    def _bubble_down(self, idx: int) -> None:
        """Restore invariant of H from idx by swapping items downwards.

        Parameters
        ----------
        idx : int

        Complexity
        ----------
        Space : O(1)
        Time : O(log n)

        """

        def helper(i: int, j: int) -> int:
            """Restores heap invariant between two item indices.

            This method swaps the item at index i with the item at index j
            if item i is meant to be the parent of item j in H. In either
            case, this method will return the index of the parent
            item between indices i and j.

            Parameters
            ----------
            i : int
            j : int

            Returns
            -------
            int
                Parent index between indices i and j.

            """

            if self._compare(self.items[i], self.items[j]):
                self._swap(i, j)
                return i
            return j

        p = idx
        l = self._left(idx)
        r = self._right(idx)

        while l != None:
            if r == None or self._compare(self.items[l], self.items[r]):
                next_p = helper(l, p)
            else:
                next_p = helper(r, p)

            if next_p != p:
                p = next_p
                l = self._left(p)
                r = self._right(p)
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """Helper method to swap items at index i and j.

        Parameters
        ----------
        i : int
        j : int

        Complexity
        ----------
        Space : O(1)
        Time : O(1)

        """

        self.items[i], self.items[j] = self.items[j], self.items[i]
        self.indices[self.items[i].uid] = i
        self.indices[self.items[j].uid] = j

    def _compare(self, x: Node, y: Node) -> bool:
        """Convert mode of H to a comparison function.

        Either computes x <= y or y >= x, if Heap mode is 'min' or
        Heap mode is 'max', respectively.

        Parameters
        ----------
        x : Node
        y : Node

        Returns
        -------
        bool

        """

        if self.mode == "min":
            return x[self.label] <= y[self.label]
        return x[self.label] >= y[self.label]
