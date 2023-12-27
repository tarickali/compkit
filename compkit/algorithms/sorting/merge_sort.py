"""
title : merge_sort.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

from copy import deepcopy

from compkit.core import Number, INF


def merge_sort(A: list[Number], inplace: bool = True) -> list[Number]:
    """Sort input array using the merge sort algorithm.

    Parameters
    ----------
    A : list[Number]
    inplace : bool = True

    Returns
    -------
    list[Number]

    """

    def merge(l: int, m: int, r: int) -> list[Number]:
        L = B[l:m] + [INF]
        R = B[m:r] + [INF]

        i = j = 0
        for k in range(l, r):
            if L[i] < R[j]:
                B[k], i = L[i], i + 1
            else:
                B[k], j = R[j], j + 1

    def recurse(l: int, r: int) -> None:
        if r - l <= 1:
            return
        m = (r + l) // 2
        recurse(l, m)
        recurse(m, r)
        merge(l, m, r)

    B = A
    if not inplace:
        B = deepcopy(A)

    recurse(0, len(B))

    return B
