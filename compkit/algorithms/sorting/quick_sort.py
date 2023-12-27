"""
title : quick_sort.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

import random
from copy import deepcopy

from compkit.core import Number


def quick_sort(A: list[Number], inplace: bool = True) -> list[Number]:
    """Sort input array using the quick sort algorithm.

    Parameters
    ----------
    A : list[Number]
    inplace : bool = True

    Returns
    -------
    list[Number]

    """

    def partition(l: int, r: int) -> int:
        p = random.randrange(l, r)
        key = B[p]
        B[l], B[p] = B[p], B[l]

        k = l
        for i in range(l + 1, r):
            if B[i] < key:
                k += 1
                B[i], B[k] = B[k], B[i]
        B[l], B[k] = B[k], B[l]
        return k

    def recurse(l: int, r: int) -> None:
        if r - l <= 1:
            return
        p = partition(l, r)
        recurse(l, p)
        recurse(p + 1, r)

    B = A
    if not inplace:
        B = deepcopy(A)

    recurse(0, len(B))

    return B
