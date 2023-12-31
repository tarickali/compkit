"""
title : types.py
create : @tarickali 23/12/27
update : @tarickali 23/12/31
"""

from typing import Any, Iterable

from compkit.core import ID, Node, Link

__all__ = ["create_nodes", "create_links"]


def create_nodes(items: Iterable[ID] | dict[ID, dict[str, Any]]) -> list[Node]:
    """Create Node objects given uids or (uid, data) pairs.

    Parameters
    ----------
    items : Iterable[ID] | dict[ID, dict[str, Any]]
        If isinstance(items, Iterable) it is of the form x.uid, otherwise
        the dictionary is of the form x.uid -> data

    Returns
    -------
    list[Node]

    """

    nodes = []
    if isinstance(items, Iterable):
        for uid in items:
            nodes.append(Node(uid))
    else:
        for uid, data in items.items():
            nodes.append(Node(uid, data))
    return nodes


def create_links(
    items: Iterable[tuple[ID, ID, ID]] | dict[ID, tuple[ID, ID, dict[str, Any]]]
) -> list[Link]:
    """Create Link objects given a dictionary of (uid, (xid, yid, data)) pairs.

    Parameters
    ----------
    items : Iterable[tuple[ID, ID, ID]] | dict[ID, tuple[ID, ID, dict[str, Any]]]
        If isinstance(items, Iterable) the tuples are of the form (e.uid, e.xid, e.yid),
        otherwise the dictionary is of the form e.uid -> (e.xid, e.yid, data)

    Returns
    -------
    list[Link]

    """

    links = []
    if isinstance(items, Iterable):
        for uid, xid, yid in items:
            links.append(Link(uid, xid, yid))
    else:
        for uid, (xid, yid, data) in items.items():
            links.append(Link(uid, xid, yid, data))
    return links
