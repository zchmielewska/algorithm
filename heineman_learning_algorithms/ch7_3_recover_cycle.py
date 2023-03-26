def recover_cycle(DG):
    marked = {}
    in_stack = {}
    node_from = {}
    cycle = []

    def _recover_cycle(w, v):
        n = v
        while n != w:
            yield n
            n = node_from[n]
        yield w
        yield v

    def dfs(v):
        in_stack[v] = True
        marked[v] = True

        if cycle:
            return

        for w in DG[v]:
            if w not in marked:
                node_from[w] = v
                dfs(w)
            else:
                if w in in_stack and in_stack[w]:
                    cycle.extend(reversed(list(_recover_cycle(w, v))))

        in_stack[v] = False

    for v in DG.nodes():
        if v not in marked and not cycle:
            dfs(v)

    return cycle

