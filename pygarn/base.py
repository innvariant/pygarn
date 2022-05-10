import copy

from typing import Set
from typing import TypeVar
from typing import Union

import networkx as nx
import numpy as np


T_Graph = TypeVar("T_Graph", bound=nx.Graph)  # T_Graph = Type[nx.Graph]


def apply_potentially_inplace(obj, fn_inplace):
    _obj = fn_inplace(obj)
    if _obj is not None:
        obj = _obj
    return obj


def get_unused_vertex(graph: T_Graph, inplace=True):
    vertex_new = len(graph.nodes)
    if graph.has_node(vertex_new):
        graph = nx.relabel_nodes(
            graph, {name: ix for ix, name in enumerate(graph.nodes)}, copy=not inplace
        )
    return vertex_new if inplace else graph, vertex_new


def sampler_random_uniform(candidates: Union[int, str], min: int, max: int):
    if min > len(candidates):
        raise ValueError(
            f"Can not sample from a candidate list of size {len(candidates)} which is smaller than the given minimum {min}"
        )
    if max is None:
        max = len(candidates)
    elif max < min:
        raise ValueError(
            f"Minimum {min} is larger than given maximum {max} for range [{min},{max}]."
        )
    size = np.random.randint(min, np.minimum(max + 1, len(candidates)))
    return np.random.choice(candidates, size, replace=False)


class GraphOperation(object):
    def applicable(self, graph: T_Graph) -> bool:
        raise NotImplementedError()

    def forward(self, graph: T_Graph, inplace: bool = False) -> T_Graph:
        assert graph is not None
        if not inplace:
            graph = copy.deepcopy(graph)
        return apply_potentially_inplace(graph, self.forward_inplace)

    def forward_inplace(self, graph: T_Graph) -> T_Graph:
        raise NotImplementedError()

    def backward(self, graph: T_Graph, inplace: bool = False) -> T_Graph:
        assert graph is not None
        if not inplace:
            graph = copy.deepcopy(graph)
        return apply_potentially_inplace(graph, self.backward_inplace)

    def backward_inplace(self, graph: T_Graph) -> T_Graph:
        raise NotImplementedError()


class VertexSelector(object):
    def __init__(self, min: int, max: int = None, sampler=sampler_random_uniform):
        self._sampler = sampler
        self._sample_min = min
        self._sample_max = max

    def forward_suggest(self, graph: T_Graph) -> Set[Union[int, str]]:
        pass

    def forward_sample(self, graph: T_Graph) -> Union[int, str]:
        return self._sampler(
            self.forward_suggest(graph), min=self._sample_min, max=self._sample_max
        )


class RandomVertexSelector(VertexSelector):
    def forward_suggest(self, graph: T_Graph) -> Set[Union[int, str]]:
        return set(graph.nodes)


class VertexDegreeSelector(VertexSelector):
    def __init__(
        self,
        descending: bool = True,
        limit: int = 3,
        min: int = 1,
        min_degree: int = None,
        max_degree: int = None,
        sampler=np.random.choice,
    ):
        super().__init__(sampler=sampler, min=min, max=None)
        self._descending = descending
        self._min_degree = min_degree
        self._max_degree = max_degree
        self._limit = int(limit) if limit is not None else None

    def forward_suggest(self, graph: T_Graph) -> Set[Union[int, str]]:
        degree_vertices = [
            (v, d)
            for v, d in graph.degree()
            if (self._min_degree is not None and d >= self._min_degree)
            and (self._max_degree is not None and d <= self._max_degree)
        ]
        order_vertices = [
            v
            for (v, d) in sorted(
                degree_vertices, key=lambda tup: tup[1], reverse=self._descending
            )
        ]
        return order_vertices if self._limit is None else order_vertices[: self._limit]
