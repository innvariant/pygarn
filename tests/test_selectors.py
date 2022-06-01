import networkx as nx
import numpy as np

from pygarn.base import VertexDegreeSelector


def test_VertexDegreeSelector_success():
    # Arrange
    n_exp_repetitions = 10
    graph_star = nx.Graph()
    graph_star.add_nodes_from(np.arange(10))
    graph_star.add_edges_from([(0, i) for i in range(1, 10)])
    selector = VertexDegreeSelector(limit=1)

    for _ in range(n_exp_repetitions):
        # Act
        vertices_selected = selector.forward_sample(graph_star)

        # Assert
        assert vertices_selected is not None
        assert 0 in vertices_selected
