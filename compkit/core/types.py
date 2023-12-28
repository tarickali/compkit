"""
title : types.py
create : @tarickali 23/12/26
update : @tarickali 23/12/27
"""

from __future__ import annotations
from typing import Hashable, Any
from collections.abc import KeysView, ValuesView, ItemsView
from dataclasses import dataclass, field

__all__ = ["ID", "Number", "Node"]

ID = int | str | tuple | Hashable
Number = int | float | complex


@dataclass(frozen=True)
class Node:
    """A dictionary-like container with a unique ID used to store data."""

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