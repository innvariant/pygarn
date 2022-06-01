import networkx as nx
import numpy as np

from pygarn.base import RandomVertexSelector
from pygarn.growth import UnfoldSubgraph


def test_add_vertex_one_by_one():
    g1 = nx.Graph()
    g1.add_nodes_from(np.arange(5))
    g1.add_edges_from([(0, 1), (1, 2), (2, 3), (2, 4), (2, 5), (3, 5)])

    op_unfold = UnfoldSubgraph(RandomVertexSelector(min=1, max=1))

    g1 = op_unfold.forward(g1)

    assert g1 is not None
    assert len(g1.nodes) > 0
