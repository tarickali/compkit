"""
title : test_union_find.py
create : @tarick 24/01/01
update : @tarick 24/01/06
"""

from compkit.structures import UnionFind
from compkit.utils.types import create_nodes


def test_union_find():
    nodes = create_nodes(range(3))
    U = UnionFind(nodes)

    assert U.find(0) != U.find(1)
    assert U.find(0) != U.find(2)
    assert U.find(1) != U.find(2)
    U.union(0, 1)
    assert U.find(0) == U.find(1)
    assert U.find(0) != U.find(2)
    U.union(1, 2)
    assert U.find(0) == U.find(1)
    assert U.find(0) == U.find(2)

    assert len(U) == 3
