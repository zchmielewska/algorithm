import networkx as nx


def create_graph():
    G = nx.Graph()
    G.add_node("A2")
    G.add_nodes_from(["A3", "A4", "A5"])

    G.add_edge("A2", "A3")
    G.add_edges_from([("A3", "A4"), ("A4", "A5")])

    for i in range(2, 6):
        G.add_edge(f"B{i}", f"C{i}")
        if 2 < i < 5:
            G.add_edge(f"B{i}", f"B{i+1}")

        if i < 5:
            G.add_edge(f"C{i}", f"C{i + 1}")

    print("Liczba węzłów:", G.number_of_nodes())
    print("Liczba krawędzi:", G.number_of_edges())
    print("Węzły sąsiadujące z C3:", list(G["C3"]))
    print("Krawędzie sąsiadujące z C3:", list(G.edges("C3")))


class Node:
    def __init__(self, val, rest=None):
        self.value = val
        self.next = rest


class Entry:
    def __init__(self, v, p):
        self.value = v
        self.priority = p


class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, val):
        self.top = Node(val. self.top)

    def pop(self):
        if self.is_empty():
            raise RuntimeError("Stos jest pusty")

        val = self.top.value
        self.top = self.top.next
        return val


class Queue:
    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        return self.first is None

    def enqueue(self, val):
        if self.first is None:
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


def dfs_search(G, src):
    """Depth-first search"""
    marked = {}
    node_from = {}

    stack = Stack()
    marked[src] = True
    stack.push(src)

    while not stack.is_empty():
        v = stack.pop()
        for w in G[v]:
            if w not in marked:
                node_from[w] = v
                marked[w] = True
                stack.push(w)

    return node_from


def bfs_search(G, src):
    """Breadth-frst search"""
    marked = {}
    node_from = {}

    q = Queue()
    marked[src] = True
    q.enqueue(src)

    while not q.is_empty():
        v = q.dequeue()
        for w in G[v]:
            if w not in marked:
                node_from[w] = v
                marked[w] = True
                q.enqueue(w)

    return node_from


def guided_search(G, src, target):
    marked = {}
    node_from = {}

    pq = PQ(G.number_of_nodes())
    marked[src] = True
    #pq.enqueue(src, -distance_to(src, target))
    pq.enqueue(src, 0)

    while not pq.is_empty():
        v = pq.dequeue()

        for w in G.neighbors(v):
            if w not in marked:
                node_from[w] = v
                marked[w] = True
                #pq.enqueue(w, -distance_to(w, target))
                pq.enqueue(w, 0)


def path_to(node_from, src, target):
    if target not in node_from:
        raise ValueError("Nieosiągalny")

    path = []
    v = target
    while v != src:
        path.append(v)
        v = node_from[v]

    path.append(src)
    path.reverse()
    return path


def dfs_search_recursive(G, src):
    """Rekurencyjna implementacja przeszukiwania w głąb dla grafu skierowanego"""
    marked = {}
    node_from = {}

    def dfs(v):
        marked[v] = True
        for w in G[v]:
            if w not in marked:
                node_from[w] = v
                dfs(w)

    dfs(src)
    return node_from


class IndexedMinPQ:
    """Indeksowana kolejka priorytetowa typu min"""
    def __init__(self, size):
        self.N = 0
        self.size = size
        self.values = [None] * (size+1)
        self.priorities = [None] * (size+1)
        self.location = {}

    def __contains__(self, v):
        return v in self.location

    def less(self, i, j):
        return self.priorities[i] > self.priorities[j]

    def swap(self, i, j):
        self.values[i], self.values[j] = self.values[j], self.values[i]
        self.priorities[i], self.priorities[j] = self.priorities[j], self.priorities[i]
        self.location[self.values[i]] = i
        self.location[self.values[j]] = j

    def enqueue(self, v, p):
        self.N += 1
        self.values[self.N], self.priorities[self.N] = v, p
        self.location[v] = self.N
        self.swim(self.N)


if __name__ == "__main__":
    # create_graph()
    pass
