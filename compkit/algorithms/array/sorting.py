"""
title : sorting.py
create : @tarickali 23/12/26
update : @tarickali 24/01/06
"""

import random
from copy import deepcopy

from compkit.core import Number, INF

__all__ = [
    "bubble_sort",
    "insertion_sort",
    "selection_sort",
    "merge_sort",
    "quick_sort",
]


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
