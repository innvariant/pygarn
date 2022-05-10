import networkx as nx

from pygarn.base import VertexDegreeSelector
from pygarn.growth import DuplicateGraph


def test_duplication_multiple_rounds():
    n_vertices_initial = 10
    g_initial = nx.connected_watts_strogatz_graph(n_vertices_initial, k=3, p=0.3)

    selector = VertexDegreeSelector(descending=False)
    op_dup = DuplicateGraph(bridge_selector=selector)
    n_rounds = 4

    g_current = g_initial.copy()
    for i_round in range(n_rounds):
        g_current = op_dup.forward(g_current)
        assert len(g_current.nodes) == len(g_initial.nodes) * 2 ** (i_round + 1)


def test_duplication_backwards():
    n_vertices_initial = 20
    g_initial = nx.connected_watts_strogatz_graph(n_vertices_initial, k=3, p=0.3)

    selector = VertexDegreeSelector(descending=False)
    op_dup = DuplicateGraph(bridge_selector=selector)

    g_dup = g_initial.copy()
    g_dup = op_dup.forward(g_dup)

    print(f"Initial graph: #v={len(g_initial.nodes)}, #e={len(g_initial.edges)}")
    print(f"Dup graph: #v={len(g_dup.nodes)}, #e={len(g_dup.edges)}")
    try:
        g_half = op_dup.backward(g_dup)
    except ValueError:
        # TODO heuristic not well thought out
        print("Could not find half graph in time")
    print(f"Half graph: #v={len(g_half.nodes)}, #e={len(g_half.edges)}")
