import networkx as nx

from pygarn.base import RandomVertexSelector
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

    n_edges_to_add_max = 3
    n_rounds = 5
    op_add = AddVertex(RandomVertexSelector(min=1, max=n_edges_to_add_max))

    for _ in range(n_rounds):
        g1 = op_add.forward(g1)

    assert len(g1.nodes) == n_rounds
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
