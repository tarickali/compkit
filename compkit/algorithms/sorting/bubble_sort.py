"""
title : bubble_sort.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

from copy import deepcopy

from compkit.core import Number


def bubble_sort(A: list[Number], inplace: bool = True) -> list[Number]:
    """Sort input array using the bubble sort algorithm.

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
    for _ in range(len(B)):
        swapped = False
        for i in range(n - 1):
            if B[i] > B[i + 1]:
                B[i], B[i + 1] = B[i + 1], B[i]
                swapped = True
        if not swapped:
            break
        n = n - 1

    return B
