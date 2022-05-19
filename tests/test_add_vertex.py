import networkx as nx
import numpy as np

from pygarn.base import RandomVertexSelector
from pygarn.base import VertexDegreeSelector
from pygarn.growth import AddVertex


def test_add_vertex_one_by_one():
    g1 = nx.Graph()

    op_add = AddVertex(RandomVertexSelector(min=1, max=1))
    n_rounds = 5

    for _ in range(n_rounds):
        g1 = op_add.forward(g1)

    assert len(g1.nodes) == n_rounds
    assert len(g1.edges) == n_rounds - 1


def test_add_vertex_one_by_one_inplace():
    g_current = nx.Graph()

    op_add = AddVertex(RandomVertexSelector(min=1, max=1))
    n_rounds = 5

    for _ in range(n_rounds):
        op_add.forward_inplace(g_current)

    assert len(g_current.nodes) == n_rounds
    assert len(g_current.edges) == n_rounds - 1


def test_add_vertex_one_by_one_copy():
    g_original = nx.Graph()

    op_add = AddVertex(RandomVertexSelector(min=1, max=1))
    n_rounds = 5

    g_modified = [g_original]
    for _ in range(n_rounds):
        g_modified.append(op_add.forward(g_modified[-1]))

    assert len(g_modified) == n_rounds + 1
    assert len(g_modified[-1].nodes) == n_rounds
    assert len(g_modified[-1].edges) == n_rounds - 1


def test_add_vertex_one_by_one_multi_edges():
    g1 = nx.Graph()
    g1.add_node(0)

    n_edges_to_add_max = 3
    n_rounds = 5
    op_add = AddVertex(RandomVertexSelector(min=1, max=n_edges_to_add_max))

    for _ in range(n_rounds):
        g1 = op_add.forward(g1)

    assert len(g1.nodes) == n_rounds + 1
    assert len(g1.edges) >= n_rounds
    assert len(g1.edges) <= n_rounds * n_edges_to_add_max - 1


def test_add_vertex_no_edges():
    g_current = nx.Graph()

    op_add = AddVertex(RandomVertexSelector(min=0, max=0))
    n_rounds = 5

    for _ in range(n_rounds):
        g_current = op_add.forward(g_current)

    assert len(g_current.nodes) == n_rounds
    assert len(g_current.edges) == 0


def test_add_vertex_high_degree():
    n_vertices_initial = 20
    g_initial = nx.erdos_renyi_graph(n_vertices_initial, 0.3)
    n_edges_initial = len(g_initial.edges)
    degrees_initial = [(v, d) for v, d in g_initial.degree()]

    selector = VertexDegreeSelector()
    op_add = AddVertex(selector)
    n_rounds = 5

    g_current = g_initial.copy()
    for _ in range(n_rounds):
        g_current = op_add.forward(g_current)

    assert len(g_current.nodes) == n_vertices_initial + n_rounds
    assert len(g_current.edges) > n_edges_initial + n_rounds
    if selector._sample_max is not None:
        assert len(g_current.edges) < n_edges_initial + n_rounds * selector._sample_max

    # Now the highest degree must have increased
    # We assert that the average degree of the n highest connected vertices must have increased
    n_highest_degrees = 5
    assert np.mean(
        np.sort([d for v, d in g_current.degree()])[:-n_highest_degrees:-1]
    ) > np.mean(np.sort([d for _, d in degrees_initial])[:-n_highest_degrees:-1])

    # On the other hand, the density must have decreased as we added edges below the average density
    assert nx.density(g_current) < nx.density(g_initial)
