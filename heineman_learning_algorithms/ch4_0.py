# Code from the book

class Node:
    def __init__(self, val):
        self.value = val
        self.next = None


class Queue:
    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        return self.first is None

    def enqueue(self, val):
        if self is None:
            self.first = self.last = Node(val)
        else:
            self.last.next = Node(val)
            self.last = self.last.next

    def dequeue(self):
        if self.is_empty():
            raise RuntimeError("Queue is empty")

        val = self.first.value
        self.first = self.first.next
        return val

