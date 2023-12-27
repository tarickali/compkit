"""
title : types.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

from __future__ import annotations
from typing import Hashable

__all__ = ["ID", "Number"]

ID = int | str | tuple | Hashable
Number = int | float | complex
