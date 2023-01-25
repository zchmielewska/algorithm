import random


class Entry:
    def __init__(self, v, p):
        self.value = v
        self.priority = p

    def __repr__(self):
        return f"{self.value}"


class PQ:
    def __init__(self, size):
        self.size = size
        self.storage = [None] * (size+1)
        self.N = 0

    def less(self, i, j):
        return self.storage[i].priority < self.storage[j].priority

    def swap(self, i, j):
        self.storage[i], self.storage[j] = self.storage[j], self.storage[i]

    def enqueue(self, v, p):
        if self.N == self.size:
            raise RuntimeError("Priority queue is full.")

        self.N += 1
        self.storage[self.N] = Entry(v, p)
        self.swim(self.N)

    def swim(self, child):
        while child > 1 and self.less(child//2, child):
            self.swap(child, child//2)
            child = child//2

    def dequeue(self):
        if self.N == 0:
            raise RuntimeError("Priority queue is empty.")

        max_entry = self.storage[1]
        self.storage[1] = self.storage[self.N]
        self.storage[self.N] = None
        self.N -= 1
        self.sink(1)
        return max_entry.value

    def sink(self, parent):
        while 2*parent <= self.N:
            child = 2*parent
            if child < self.N and self.less(child, child+1):
                child += 1

            if not self.less(parent, child):
                break

            self.swap(child, parent)
            parent = child

    def peek(self):
        return self.storage[1]

    def is_empty(self):
        return self.N == 0


def iterator(pq):
    N = pq.N

    pqit = PQ(N)
    pqit.enqueue(1, pq.peek().priority)

    while pqit:
        idx = pqit.dequeue()
        yield pq.storage[idx].value, pq.storage[idx].priority

        child = 2*idx
        if child <= pq.N:
            pqit.enqueue(child, pq.storage[child].priority)
        child += 1
        if child <= pq.N:
            pqit.enqueue(child, pq.storage[child].priority)


if __name__ == "__main__":
    size = 7
    pq = PQ(size)

    for _ in range(size):
        r = random.randint(0, 100)
        pq.enqueue(r, r)

    print(pq.storage)

    for p in iterator(pq):
        print(p)
