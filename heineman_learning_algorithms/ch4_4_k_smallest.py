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


def k_smallest(vals, k):
    N = len(vals)
    pq = PQ(N)

    for v in vals:
        if pq.N < k:
            pq.enqueue(v, v)
        else:
            if v < pq.peek().priority:
                pq.dequeue()
                pq.enqueue(v, v)

    result = []
    while not pq.is_empty():
        result.append(pq.dequeue())

    return list(reversed(result))


if __name__ == "__main__":
    vals = random.sample(range(0, 10 * 10), 10)
    result = k_smallest(vals, 5)
    print("Values:", vals)
    print("K-smallest:", result)
