# Kolejka cykliczna

class Queue:
    def __init__(self, size):
        self.size = size
        self.storage = [None] * size
        self.first = 0
        self.last = 0
        self.N = 0

    def is_empty(self):
        return self.N == 0

    def is_full(self):
        return self.N == self.size

    def enqueue(self, item):
        if self.is_full():
            raise RuntimeError("Queue is full")

        self.storage[self.last] = item
        self.N += 1
        self.last = (self.last + 1) % self.size

    def dequeue(self):
        if self.is_empty():
            raise RuntimeError("Queue is empty")

        val = self.storage[self.first]
        self.N -= 1
        self.first = (self.first + 1) % self.size
        return val

