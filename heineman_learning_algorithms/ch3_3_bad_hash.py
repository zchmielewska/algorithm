class ValueBadHash:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return hash(self.v) % 4

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.v == other.v


class LinkedEntry:
    def __init__(self, k, v, rest=None):
        self.key = k
        self.value = v
        self.next = rest


class HashtableLinked:
    """Separate chaining"""
    def __init__(self, m=10):
        self.table = [None] * m
        self.M = m
        self.N = 0

    def get(self, k):
        hc = hash(k) % self.M
        entry = self.table[hc]
        while entry:
            if entry.key == k:
                return entry.value
            entry = entry.next
        return None

    def put(self, k, v):
        hc = hash(k) % self.M
        entry = self.table[hc]
        while entry:
            if entry.key == k:
                entry.value = v
                return
            entry = entry.next

        self.table[hc] = LinkedEntry(k, v, self.table[hc])
        self.N += 1


if __name__ == "__main__":
    pass