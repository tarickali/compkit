"""
title : inversions.py
create : @tarickali 24/01/07
update : @tarickali 24/01/07
"""

from compkit.core import Number

__all__ = ["binary_search"]


def binary_search(
    A: list[Number], target: Number, recursive: bool = False
) -> tuple[bool, int]:
    """Search for target in a sorted array A.

    Parameters
    ----------
    A : list[Number]
        The array to search over
    target : Number
        The number to search for in A
    recursive : bool = False
        Determines if the traversal should be performed recursively or
        iteratively

    Returns
    -------
    (contains, index) : tuple[bool, int]
        If target is in A, contains = True, otherwise contains = False. If
        contains = True, index is where target is in A, otherwise it is where
        target would be inserted in A (shifting larger values right)

    Warnings
    --------
    - This function assumes that the input array A is sorted. If A is not sorted,
    then this functions behavior is not well-defined.

    """

    def recursion(l: int, r: int) -> tuple[bool, int]:
        if l >= r:
            return False, l

        m = l + (r - l) // 2
        if A[m] == target:
            return True, m
        elif A[m] < target:
            return recursion(m + 1, r)
        else:
            return recursion(l, m)

    def iteration() -> tuple[bool, int]:
        l = 0
        r = len(A)

        while l < r:
            m = l + (r - l) // 2
            if A[m] == target:
                return True, m
            elif A[m] < target:
                l = m + 1
            else:
                r = m
        return False, l

    if recursive:
        return recursion(0, len(A))
    else:
        return iteration()
