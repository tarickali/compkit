"""
title : insertion_sort.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

from copy import deepcopy

from compkit.core import Number


def insertion_sort(A: list[Number], inplace: bool = True) -> list[Number]:
    """Sort input array using the insertion sort algorithm.

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
    for i in range(1, n):
        x = B[i]
        j = i - 1
        while j >= 0 and B[j] > x:
            B[j + 1] = B[j]
            j -= 1
        B[j + 1] = x

    return B
