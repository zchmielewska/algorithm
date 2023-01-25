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


def merged_arrays(heap1, heap2):
    result = [None] * (heap1.N + heap2.N)
    idx = len(result) - 1
    while idx >= 0:
        if heap1.is_empty():
            result[idx] = heap2.dequeue()
        elif heap2.is_empty():
            result[idx] = heap1.dequeue()
        else:
            if heap1.peek().priority > heap2.peek().priority:
                result[idx] = heap1.dequeue()
            else:
                result[idx] = heap2.dequeue()
        idx -= 1
    return result


if __name__ == "__main__":
    m = 2**3
    n = 2**4

    heap1 = PQ(m)
    heap2 = PQ(n)

    for _ in range(m):
        r1 = round(random.random(), 2)
        heap1.enqueue(r1, r1)

    for _ in range(n):
        r2 = round(random.random(), 2)
        heap2.enqueue(r2, r2)

    print("heap1:", heap1.storage)
    print("heap2:", heap2.storage)

    result = merged_arrays(heap1, heap2)
    print("result:", result)
