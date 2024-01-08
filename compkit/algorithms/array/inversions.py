"""
title : inversions.py
create : @tarickali 24/01/07
update : @tarickali 24/01/07
"""

from copy import deepcopy

from compkit.core import Number, INF

__all__ = ["inversions"]


def inversions(A: list[Number], inplace: bool = True) -> int:
    """Compute the number of inversions in A.

    An inversion of an array A is a pair of indices i, j such that
    i < j and A[j] < A[i].

    Parameters
    ----------
    A : list[Number]
    inplace : bool = True
        Determines if A is modified, resulting in A being sorted

    Returns
    -------
    int

    """

    def merge(l: int, m: int, r: int) -> int:
        L = B[l:m] + [INF]
        R = B[m:r] + [INF]

        i = j = 0
        count = 0
        for k in range(l, r):
            if L[i] < R[j]:
                B[k], i = L[i], i + 1
            else:
                B[k], j = R[j], j + 1
                count += (m - l) - i

        return count

    def recurse(l: int, r: int) -> int:
        if r - l <= 1:
            return 0
        m = (r + l) // 2
        left = recurse(l, m)
        right = recurse(m, r)
        middle = merge(l, m, r)

        return left + right + middle

    B = A
    if not inplace:
        B = deepcopy(A)

    count = recurse(0, len(B))

    return count
