def count(n, target):
    ct = 0
    if n is None:
        return 0
    if n.value == target:
        ct = 1
    return ct + count(n.next, target)


