"""
title : create_types.py
create : @tarickali 23/12/27
update : @tarickali 23/12/27
"""

from typing import Any

from compkit.core import ID, Node

__all__ = ["create_nodes"]


def create_nodes(items: dict[ID, dict[str, Any]]) -> list[Node]:
    """Create Node objects given a dictionary of (uid, data) pairs.

    Parameters
    ----------
    items : dict[ID, dict[str, Any]]

    Returns
    -------
    list[Node]

    """

    nodes = []
    for uid, data in items.items():
        nodes.append(Node(uid, data))
    return nodes
