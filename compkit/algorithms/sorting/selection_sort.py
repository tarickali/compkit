"""
title : selection_sort.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

from copy import deepcopy

from compkit.core import Number


def selection_sort(A: list[Number], inplace: bool = True) -> list[Number]:
    """Sort input array using the selection sort algorithm.

    Parameters
    ----------
    A : list[Number]
    inplace : bool = True

    Returns
    -------
    list[Number]

    """

    B = A
    if not inplace:
        B = deepcopy(A)

    n = len(B)
    for i in range(n):
        k = i
        for j in range(i + 1, n):
            if B[j] < B[k]:
                k = j
        B[i], B[k] = B[k], B[i]

    return B
