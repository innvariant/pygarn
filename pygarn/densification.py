from typing import Set
from typing import TypeVar
from typing import Union

import networkx as nx

from pygarn.base import GraphOperation
from pygarn.base import RandomVertexSelector
from pygarn.base import VertexSelector


T_Graph = TypeVar("T_Graph", bound=nx.Graph)


class AddEdge(GraphOperation):
    def __init__(
        self,
        source: VertexSelector = RandomVertexSelector(min=1, max=1),
        target: VertexSelector = RandomVertexSelector(min=1, max=1),
    ):
        self._source = source
        self._target = target

    def applicable(self, graph: T_Graph) -> bool:
        return True

    def forward_inplace(self, graph: T_Graph) -> T_Graph:
        pass

    def backward_inplace(
        self, graph: T_Graph, return_fuzzy: bool = False
    ) -> Union[T_Graph, Set[T_Graph]]:
        pass
