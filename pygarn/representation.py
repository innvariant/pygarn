from typing import List
from typing import Set

import networkx as nx

from pygarn.base import GraphOperation


def deconstruct(graph: nx.Graph, ops: Set[GraphOperation]) -> List[GraphOperation]:
    assert graph is not None
    if len(graph.nodes) == 0:
        return []

    assert ops is not None and len(ops) > 0
