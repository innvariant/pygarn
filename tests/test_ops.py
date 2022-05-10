import matplotlib.pyplot as plt
import networkx as nx

from pygarn.growth import AddConnectedVertex


def test_dev():
    g1 = nx.Graph()

    op_1 = AddConnectedVertex()

    for _ in range(5):
        op_1.forward(g1)

    nx.draw(g1)
    plt.show()
