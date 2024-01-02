"""
title : test_sorting.py
create : @tarickali 23/12/26
update : @tarickali 23/12/26
"""

import random

from compkit.algorithms.sorting import *


def generate_data() -> list[int]:
    low = random.randint(0, 100)
    high = random.randint(low + 1, 500)
    size = random.randint(0, 1000)
    A = [random.randint(low, high) for _ in range(size)]
    return A


def test_bubble_sort():
    for _ in range(100):
        A = generate_data()
        A = bubble_sort(A)
        assert A == sorted(A)


def test_insertion_sort():
    for _ in range(100):
        A = generate_data()
        A = insertion_sort(A)
        assert A == sorted(A)


def test_selection_sort():
    for _ in range(100):
        A = generate_data()
        A = selection_sort(A)
        assert A == sorted(A)


def test_merge_sort():
    for _ in range(100):
        A = generate_data()
        A = merge_sort(A)
        assert A == sorted(A)


def test_quick_sort():
    for _ in range(100):
        A = generate_data()
        A = quick_sort(A)
        assert A == sorted(A)
