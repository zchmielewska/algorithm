import networkx as nx


def dfs_search_recursive(G, src):
    marked = {}
    node_from = {}

    def dfs(v):
        marked[v] = True
        for w in G[v]:
            if w not in marked:
                node_from[w] = v
                dfs(w)

    dfs(src)
    return node_from
