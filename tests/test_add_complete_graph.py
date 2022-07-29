import networkx as nx
import numpy as np

from pygarn.base import RandomVertexSelector
from pygarn.growth import AddCompleteGraph


def test_add_triangle():
    n_nodes_init = 5
    list_edges_init = [(0, 1), (1, 2), (2, 3), (2, 4)]
    g1 = nx.Graph()
    g1.add_nodes_from(np.arange(n_nodes_init))
    g1.add_edges_from(list_edges_init)
    assert len(g1.nodes) == n_nodes_init
    assert len(g1.edges) == len(list_edges_init)

    op_add_triangle = AddCompleteGraph(
        size=3,
        sources=RandomVertexSelector(min=1, max=1),
        targets=RandomVertexSelector(min=1, max=1),
    )

    g1 = op_add_triangle.forward(g1)

    assert g1 is not None
    assert len(g1.nodes) == n_nodes_init + 3
    assert len(g1.edges) == len(list_edges_init) + 4


def test_add_k5():
    k = 5
    n_nodes_init = 5
    list_edges_init = [(0, 1), (1, 2), (2, 3), (2, 4)]
    g1 = nx.Graph()
    g1.add_nodes_from(np.arange(n_nodes_init))
    g1.add_edges_from(list_edges_init)
    assert len(g1.nodes) == n_nodes_init
    assert len(g1.edges) == len(list_edges_init)

    op_add_triangle = AddCompleteGraph(
        size=k,
        sources=RandomVertexSelector(min=1, max=1),
        targets=RandomVertexSelector(min=1, max=1),
    )

    g1 = op_add_triangle.forward(g1)

    assert g1 is not None
    assert len(g1.nodes) == n_nodes_init + k
    assert len(g1.edges) == len(list_edges_init) + int((k * (k - 1)) / 2) + 1


def test_add_kcomplete_and_reverse():
    for k in [3, 4, 5, 6]:
        # Arrange
        n_nodes_init = np.random.randint(3, 10)
        g0 = None
        while g0 is None or not nx.is_connected(g0):
            g0 = nx.erdos_renyi_graph(n_nodes_init, 0.3)
        n_edges_init = len(g0.edges)

        op_add_kcomplete = AddCompleteGraph(
            size=k,
            sources=RandomVertexSelector(min=1, max=3),
            targets=RandomVertexSelector(min=1, max=3),
        )

        # Act
        g1 = op_add_kcomplete.forward(g0)

        # Assert
        assert g1 is not None
        assert len(g1.nodes) == n_nodes_init + k
        assert len(g1.edges) > n_edges_init + int((k * (k - 1)) / 2)
        assert nx.is_connected(g1)

        # Act again
        g_fuzzy = op_add_kcomplete.backward(g1, return_fuzzy=True)
        any_isomorphic = False
        for g2 in g_fuzzy:
            assert g2 is not None
            assert len(g2.nodes) == n_nodes_init
            any_isomorphic = any_isomorphic or nx.is_isomorphic(g2, g0)

        assert (
            any_isomorphic
        ), "Expected one of the returned graphs of the backward operation to be isomorphic to the source"
