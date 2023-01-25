_sums = [0, 1, 3, 9, 33, 153, 873, 5913, 46233, 409113, 4037913, 43954713 ]
_constants =  [0, 2, 6, 16, 50, 204, 1078, 6992, 53226, 462340, 4500254, 48454968, 524236882]


def fh_parent(k, lev):
    if lev <= 0:
        return 1
    return (k + _constants[lev-1]) // (lev+1)


def fh_child(k, lev):
    return k*(lev+2) - _constants[lev]


class Entry:
    def __init__(self, v, p):
        self.value = v
        self.priority = p


class PQ:
    def __init__(self, size):
        self.size = size
        self.storage = [None] * (size+1)
        self.N = 0
        self.level = 0

    def __len__(self):
        return self.N

    def is_full(self):
        return self.size == self.N

    def enqueue(self, v, p):
        if self.N == self.size:
            raise RuntimeError("Queue is full.")

        self.N += 1
        if self.N > _sums[self.level+1]:
            self.level += 1

        self.storage[self.N] = Entry(v, p)
        self.swim(self.N)

    def less(self, i, j):
        return self.storage[i].priority < self.storage[j].priority

    def swap(self, i, j):
        self.storage[i], self.storage[j] = self.storage[j], self.storage[i]

    def swim(self, k):
        lev = self.level
        parent = fh_parent(k, lev)
        while k > 1 and self.less(parent, k):
            self.swap(parent, k)
            k = parent
            lev -= 1
            parent = fh_parent(k, lev)

    def sink(self, k):
        lev = 0

        fc = fh_child(k, lev)
        while fc <= self.N:
            largest = fc
            offset = 1
            lev += 1
            while fc+offset < self.N and offset <= lev:
                if self.less(largest, fc+offset):
                    largest = fc+offset
                offset += 1

            if not self.less(k, largest):
                break

            self.swap(k, largest)

            k = largest
            fc = fh_child(k, lev)

    def dequeue(self):
        if self.N == 0:
            raise RuntimeError("Queue is empty")

        max_entry = self.storage[1]
        self.swap(1, self.N)
        self.N -= 1

        if self.N == _sums[self.level]:
            self.level -= 1

        self.storage[self.N+1] = None
        self.sink(1)

        return max_entry.value
