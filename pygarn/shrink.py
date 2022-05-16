from typing import TypeVar

import networkx as nx

from pygarn.base import GraphOperation
from pygarn.base import RandomVertexSelector
from pygarn.base import VertexDegreeSelector
from pygarn.base import VertexSelector
from pygarn.base import get_unused_vertex_and_relabel


T_Graph = TypeVar("T_Graph", bound=nx.Graph)  # T_Graph = Type[nx.Graph]


class RemoveVertex(GraphOperation):
    def __init__(self, selector: VertexSelector = RandomVertexSelector(min=1, max=1)):
        self._selector = selector

    def applicable(self, graph: T_Graph) -> bool:
        return graph is not None and len(graph.nodes) > 0

    def forward_inplace(self, graph: T_Graph) -> T_Graph:
        vertices = self._selector.forward_sample(graph)
        graph.remove_nodes_from(vertices)

    def backward_inplace(self, graph: T_Graph) -> T_Graph:
        assert len(graph.nodes) > 0

        selector_degree = VertexDegreeSelector(
            limit=None,
            min=1,
            max=1,
            min_degree=self._selector_connect_to._sample_min,
            max_degree=self._selector_connect_to._sample_max,
        )
        vertices = selector_degree.forward_sample(graph)
        if len(vertices) < 1:
            raise ValueError("Operation could not be applied to graph")

        vertex_new = get_unused_vertex_and_relabel(graph)
        graph.add_node(vertex_new)
        # TODO add edges based on some heuristic
