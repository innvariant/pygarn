import matplotlib.pyplot as plt
import networkx as nx

from pygarn.base import RandomVertexSelector
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
