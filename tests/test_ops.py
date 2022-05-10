import matplotlib.pyplot as plt
import networkx as nx

from pygarn.base import RandomVertexSelector
from pygarn.base import VertexDegreeSelector
from pygarn.growth import AddVertex


def test_dev():
    g1 = nx.Graph()
    g1.add_nodes_from([0, 1])
    n_rounds = 5

    op_add = AddVertex(RandomVertexSelector(2, 3))

    for _ in range(n_rounds):
        op_add.forward_inplace(g1)

    nx.draw(g1)
    plt.show()

    for _ in range(n_rounds):
        op_add.backward_inplace(g1)
        nx.draw(g1)
        plt.show()


def test_larger():
    n_vertices_initial = 10
    g_initial = nx.erdos_renyi_graph(n_vertices_initial, 0.3)

    selector = VertexDegreeSelector()
    op_add = AddVertex(selector)
    n_rounds = 3

    g_current = g_initial.copy()
    for _ in range(n_rounds):
        op_add.forward_inplace(g_current)

    for _ in range(n_rounds):
        op_add.backward_inplace(g_current)

    print(f"Initial graph: #v={len(g_initial.nodes)}, #e={len(g_initial.edges)}")
    print(f"Modified graph: #v={len(g_current.nodes)}, #e={len(g_current.edges)}")

    print(nx.graph_edit_distance(g_initial, g_current))
