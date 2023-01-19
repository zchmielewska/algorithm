class Entry:
    def __init__(self, k, v):
        self.key = k
        self.value = v


class HashtableOpenAddressingRemove:
    def __init__(self, M=10):
        if M < 2:
            raise ValueError("There should be space for at least two pairs.")

        self.table = [None] * M
        self.M = M
        self.N = 0
        self.load_factor = 0.75
        self.shrink_factor = 0.25

        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k:
                return self.table[hc].value
            hc = (hc + 1) % self.M
        return None

    def is_full(self):
        return self.N >= self.M - 1

    def put(self, k, v):
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k:
                self.table[hc].value = v
                return
            hc = (hc + 1) % self.M

        self.table[hc] = Entry(k, v)
        self.N += 1

        if self.N >= self.threshold:
            self.resize(2*self.M + 1)

    def resize(self, new_size):
        temp = HashtableOpenAddressingRemove(new_size)
        for n in self.table:
            if n:
                temp.put(n.key, n.value)
        self.table = temp.table
        temp.table = None
        self.M = temp.M
        self.threshold = self.load_factor * self.M

    def remove(self, k):
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k:
                break
            hc = (hc + 1) % self.M

        if self.table[hc] is None:
            return None

        result = self.table[hc].value
        self.table[hc] = None
        self.N -= 1

        hc = (hc + 1) % self.M
        while self.table[hc]:
            entry = self.table[hc]
            self.table[hc] = None
            self.N -= 1
            self.put(entry.key, entry.value)
            hc = (hc + 1) % self.M

        if 0 < self.N <= self.shrink_factor * self.M:
            new_size = self.M // 2
            if new_size % 2 == 0:
                new_size += 1
            self.resize(new_size)

        return result

    def __iter__(self):
        for entry in self.table:
            if entry:
                yield entry.key, entry.value

