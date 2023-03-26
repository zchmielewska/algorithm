WEIGHT = 'weight'


class NegativeCycleError(RuntimeError):
    def __init__(self, G, path, weight):
        super().__init__()
        self.graph = G
        self.path = path
        self.weight = weight

    def __str__(self):
        result = ""
        for n in self.path[:-1]:
            result += '->' + str(n)
        return f"{self.path[-2]}{result} with weight={self.weight}"


def bellman_ford_returns_negative_cycle(G, src):
    inf = float("inf")
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
                    target = e[1]
                    v = e[0]
                    path = [target]
                    weight = e[2][WEIGHT]
                    while v != target:
                        path.append(v)
                        e = edge_to[v]
                        weight += e[2][WEIGHT]
                        v = e[0]
                    path.append(target)
                    raise NegativeCycleError(G, path, weight)

    return dist_to, edge_to
