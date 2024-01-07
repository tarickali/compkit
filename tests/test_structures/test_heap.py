"""
title : test_heap.py
create : @tarickali 23/12/27
update : @tarickali 24/01/06
"""

import random

from compkit.core import Node
from compkit.structures import Heap
from compkit.utils.types import create_nodes


def generate_data() -> list[Node]:
    values = [random.randint(0, 10000) for _ in range(1000)]
    return create_nodes({i: {"val": i} for i in values})


def test_heap():
    # Test mode=min
    for _ in range(10):
        print(generate_data())
        heap = Heap.heapify(generate_data(), label="val", mode="min")

        sorted_items = []
        while not heap.empty():
            sorted_items.append(heap.extract()["val"])

        assert sorted_items == sorted(sorted_items)

    # Test mode=max
    for _ in range(10):
        heap = Heap.heapify(generate_data(), label="val", mode="max")

        sorted_items = []
        while not heap.empty():
            sorted_items.append(heap.extract()["val"])

        assert sorted_items == sorted(sorted_items, reverse=True)

    # Test without heapify
    for _ in range(10):
        heap = Heap(label="val", mode="min")
        for item in generate_data():
            heap.insert(item)

        sorted_items = []
        while not heap.empty():
            sorted_items.append(heap.extract()["val"])

        assert sorted_items == sorted(sorted_items)
