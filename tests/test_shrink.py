import networkx as nx
import numpy as np

from pygarn.base import RandomVertexSelector
from pygarn.shrink import RemoveVertex


def test_remove_vertex_one_by_one():
    n_vertices_initial = 5
    g1 = nx.Graph()
    g1.add_nodes_from(np.arange(n_vertices_initial))

    op_remove = RemoveVertex(RandomVertexSelector(min=1, max=1))
    n_rounds = n_vertices_initial

    for _ in range(n_rounds):
        g1 = op_remove.forward(g1)

    assert len(g1.nodes) == 0
    assert len(g1.edges) == 0
