"""
title : types.py
create : @tarickali 23/12/27
update : @tarickali 23/12/30
"""

from typing import Any

from compkit.core import ID, Node, Link

__all__ = ["create_nodes", "create_links"]


def create_nodes(items: list[ID] | dict[ID, dict[str, Any]]) -> list[Node]:
    """Create Node objects given uids or (uid, data) pairs.

    Parameters
    ----------
    items : list[ID] | dict[ID, dict[str, Any]]

    Returns
    -------
    list[Node]

    """

    nodes = []
    if isinstance(items, list):
        for uid in items:
            nodes.append(Node(uid))
    else:
        for uid, data in items.items():
            nodes.append(Node(uid, data))
    return nodes


def create_links(
    items: list[tuple[ID, ID, ID]] | dict[ID, tuple[ID, ID, dict[str, Any]]]
) -> list[Link]:
    """Create Link objects given a dictionary of (uid, (xid, yid, data)) pairs.

    Parameters
    ----------
    items : list[tuple[ID, ID, ID]] | dict[ID, tuple[ID, ID, dict[str, Any]]]

    Returns
    -------
    list[Link]

    """

    links = []
    if isinstance(items, list):
        for uid, xid, yid in items:
            links.append(Link(uid, xid, yid))
    else:
        for uid, (xid, yid, data) in items.items():
            links.append(Link(uid, xid, yid, data))
    return links
