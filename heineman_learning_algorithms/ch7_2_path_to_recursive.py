def path_to_recursive(node_from, src, target):
    if target == src:
        yield src
    else:
        for n in path_to_recursive(node_from, src, node_from[target]):
            yield n
        yield target
