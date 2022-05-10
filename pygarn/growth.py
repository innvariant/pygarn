from typing import TypeVar

import networkx as nx

from pygarn.base import GraphOperation
from pygarn.base import RandomVertexSelector
from pygarn.base import VertexSelector
from pygarn.base import get_unused_vertex


T_Graph = TypeVar("T_Graph", bound=nx.Graph)  # T_Graph = Type[nx.Graph]


class AddConnectedVertex(GraphOperation):
    def __init__(self, selector: VertexSelector = RandomVertexSelector(min=1, max=3)):
        self._selector = selector

    def applicable(self, graph: T_Graph) -> bool:
        pass

    def forward_inplace(self, graph: T_Graph) -> T_Graph:
        vertex_new = get_unused_vertex(graph, inplace=True)
        targets = None
        if len(graph.nodes) > 0:
            targets = self._selector.forward_sample(graph)
        graph.add_node(vertex_new)
        if targets is not None:
            graph.add_edges_from([(vertex_new, t) for t in targets])

    def backward_inplace(self, graph: T_Graph) -> T_Graph:
        pass
