class LinkedEntry:
    def __init__(self, k, v, rest=None):
        self.key = k
        self.value = v
        self.next = rest


class Hashtable:
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

    def __iter__(self):
        for entry in self.table:
            while entry:
                yield entry.key, entry.value
                entry = entry.next


def most_duplicated(A):
    ht = Hashtable()

    for v in A:
        if ht.get(v) is None:
            ht.put(v, 1)
        else:
            ht.put(v, 1 + ht.get(v))

    most = ht.get(A[0])
    result = A[0]
    for k, count in ht:
        if count > most:
            result = k
            most = count

    return result


if __name__ == "__main__":
    print(most_duplicated([1, 2, 3, 4]))
    print(most_duplicated([7, 8, 7, 9]))

