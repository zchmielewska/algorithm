# Open addressing with possiblity to remove item
# Element is marked as deleted so that the chain is not broken
# Separate chaining is faster than open addressing with remove

class MarkedEntry:
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.marked = False

    def is_marked(self):
        return self.marked

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False


class Hashtable:
    def __init__(self, M=10):
        if M < 2:
            raise ValueError("Hastable must contain >= 2 pairs.")

        self.table = [None] * M
        self.M = M
        self.N = 0
        self.deleted = 0
        self.load_factor = 0.75
        self.threshold = min(M * self.load_factor, M-1)

    def __len__(self):
        return self.N

    def get(self, k):
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k and not self.table[hc].is_marked():
                return self.table[hc].value
            hc = (hc + 1) % self.M
        return None

    def resize(self, new_size):
        temp = Hashtable(new_size)
        for n in self.table:
            if n and not n.is_marked():
                temp.put(n.key, n.value)

        self.table = temp.table
        temp.table = None
        self.M = temp.M
        self.threshold = self.load_factor * self.M
        self.deleted = 0

    def remove(self, k):
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k:
                if self.table[hc].is_marked():
                    return None

                self.table[hc].mark()
                self.N -= 1
                self.deleted += 1
                return self.table[hc].value
            hc = (hc + 1) % self.M
        return None

    def put(self, k, v):
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k:
                self.table[hc].value = v
                if self.table[hc].is_marked():
                    self.table[hc].unmark()
                    self.deleted -= 1
                    self.N += 1
                return

            hc = (hc + 1) % self.M

        self.table[hc] = MarkedEntry(k, v)
        self.N += 1

        if self.N + self.deleted >= self.threshold:
            self.resize(2*self.M + 1)

    def __iter__(self):
        for entry in self.table:
            if entry is not None and not entry.is_marked():
                yield entry.key, entry.value
