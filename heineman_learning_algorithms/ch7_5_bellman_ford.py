import networkx as nx


WEIGHT = "weight"


def bellman_ford(G, src):
    inf = float('inf')
    dist_to = {v:inf for v in G.nodes()}
    dist_to[src] = 0
    edge_to = {}

    def relax(e):
        u, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[u] + weight < dist_to[v]:
            dist_to[v] = dist_to[u] + weight
            edge_to[v] = e
            return True
        return False

    for i in range(G.number_of_nodes()):
        for e in G.edges(data=True):
            if relax(e):
                if i == G.number_of_nodes()-1:
                    raise RuntimeError('Negative Cycle exists in graph.')

    return dist_to, edge_to


def challenge_bellaman_ford():
    DG = nx.DiGraph()
    DG.add_edge("d", "e", weight=1)
    DG.add_edge("c", "d", weight=1)
    DG.add_edge("b", "c", weight=1)
    DG.add_edge("s", "b", weight=1)
    dist_to, _ = bellman_ford(DG, 's')

