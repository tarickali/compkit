"""
title : types.py
create : @tarickali 23/12/26
update : @tarickali 24/01/06
"""

from __future__ import annotations
from typing import Hashable, Any
from collections.abc import KeysView, ValuesView, ItemsView
from dataclasses import dataclass, field

__all__ = ["ID", "Number", "Node", "Link"]

ID = int | str | tuple | Hashable
Number = int | float | complex


@dataclass(frozen=True)
class Node:
    """A dictionary-like container with a unique ID used to store data.

    Parameters
    ----------
    uid : ID
        The unique ID of the Node
    data : dict[str, Any] = {}
        The data dictionary of the Node

    """

    uid: ID
    data: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def clear(self) -> None:
        self.data.clear()

    def keys(self) -> KeysView:
        return self.data.keys()

    def values(self) -> ValuesView:
        return self.data.values()

    def items(self) -> ItemsView:
        return self.data.items()

    def __hash__(self) -> int:
        return hash(self.uid)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value


@dataclass(frozen=True)
class Link:
    """A dictionary-like container with an ID used to store data between two Nodes.

    Parameters
    ----------
    uid : ID
        The unique ID of the Link
    xid : ID
        The ID of the first/left/tail Node
    yid : ID
        The ID of the second/right/head Node
    data : dict[str, Any] = {}
        The data dictionary of the Link

    """

    uid: ID
    xid: ID
    yid: ID
    data: dict[str, Any] = field(default_factory=dict)

    def nodes(self, reverse: bool = False) -> tuple[ID, ID]:
        return (self.xid, self.yid) if not reverse else (self.yid, self.xid)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def clear(self) -> None:
        self.data.clear()

    def keys(self) -> KeysView:
        return self.data.keys()

    def values(self) -> ValuesView:
        return self.data.values()

    def items(self) -> ItemsView:
        return self.data.items()

    def __hash__(self) -> int:
        return hash(self.uid)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value
