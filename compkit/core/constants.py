"""
title : constants.py
create : @tarickali 23/12/26
update : @tarickali 24/01/01
"""

import math
from sys import maxsize

__all__ = [
    "INF",
    "MAXINT",
    "MININT",
    "PI",
    "E",
    "EMPTY",
    "SPECIAL",
    "DISTANCE",
    "CAPACITY",
    "FORWARD",
    "REVERSE",
    "PARENT",
    "CHILD",
    "CHILDREN",
]

INF = float("inf")
MAXINT = maxsize
MININT = -maxsize - 1
PI = math.pi
E = math.e

EMPTY = "empty"
SPECIAL = "special"

DISTANCE = "distance"
CAPACITY = "capacity"
FORWARD = "forward"
REVERSE = "reverse"

PARENT = "parent"
CHILD = "child"
CHILDREN = "children"
