import timeit
import networkx as nx


WEIGHT = "weight"


def topological_sort(DG):
    """
    Use recursive Depth First Search to generate a topological sort of nodes.
    Only call when no cycle exists!
    """
    marked = {}
    postorder = []

    def dfs(v):
        marked[v] = True

        for w in DG[v]:
            if not w in marked:
                dfs(w)

        postorder.append(v)

    for v in DG.nodes():
        if not v in marked:
            dfs(v)

    return reversed(postorder)


def mesh_graph(n):
    """Return a mesh graph with N^2 nodes(labeled 1 to N^2) and edges that form a mesh."""
    G = nx.DiGraph()

    # add nodes/edges in expanding left of mesh
    label = 1
    num = 1
    while num < n:
        for idx in range(num):
            G.add_edge(label, label+num, weight=1)     # two edges for each node
            G.add_edge(label, label+num+1, weight=1)
            label += 1
        num += 1

    # add nodes in collapsing right of mesh
    while n > 1:
        for idx in range(n):
            if idx != 0:
                G.add_edge(label, label+n-1, weight=1)     # two edges for each node
            if idx != n-1:
                G.add_edge(label, label+n, weight=1)
            label += 1
        n -= 1

    return G


def topological_sp(DAG, src):
    """Given a DAG, compute shortest path from src."""
    inf = float('inf')
    dist_to = {v:inf for v in DAG.nodes()}
    dist_to[src] = 0
    edge_to = {}

    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e

    for n in topological_sort(DAG):
        for e in DAG.edges(n, data=True):
            relax(e)

    return dist_to, edge_to


class IndexedMinPQ:
    """
    Heap storage for an indexed min priority queue.

    Attributes
    ----------
        size       - available storage (note 0th index unused)
        N          - Number of (value, priority) pairs in the PQ
        values     - stores the ith value in the PQ
        priorities - stores the priority of the ith value in the PQ
        location   - records index in values/priorities for given value
    """
    def __init__(self, size):
        self.N = 0
        self.size = size
        self.values = [None] * (size+1)
        self.priorities = [None] * (size+1)   # binary heap using 1-based indexing
        self.location = {}                    # For each value, remember its location in storage

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def __contains__(self, v):
        """Determine if idx is currently in the priority queue."""
        return v in self.location

    def is_empty(self):
        """Returns whether priority queue is empty."""
        return self.N == 0

    def is_full(self):
        """If priority queue has run out of storage, return True."""
        return self.size == self.N

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if self.N == self.size:
            raise RuntimeError('Priority Queue is full!')
        self.N += 1

        self.values[self.N], self.priorities[self.N] = v, p
        self.location[v] = self.N                 # record where it is being stored
        self.swim(self.N)

    def decrease_priority(self, v, lower_priority):
        """Reduce associated priority with v to move it closer to head of priority queue."""
        if not v in self.location:
            raise ValueError('{} not in the indexed min priority queue.'.format(v))
        idx = self.location[v]
        if lower_priority >= self.priorities[idx]:
            raise RuntimeError('Value {} has existing priority of {} which is already lower than {}'.format(v, self.priorities[idx], lower_priority))

        self.priorities[idx] = lower_priority
        self.swim(idx)

    def less(self, i, j):
        """
        Helper function to determine if priorities[j] has higher
        priority than priorities[i]. Min PQ means > is operator to use.
        """
        return self.priorities[i] > self.priorities[j]

    def swap(self, i, j):
        """Switch the values in storage[i] and storage[j]."""
        self.values[i],self.values[j] = self.values[j],self.values[i]
        self.priorities[i],self.priorities[j] = self.priorities[j],self.priorities[i]

        self.location[self.values[i]] = i
        self.location[self.values[j]] = j

    def swim(self,child):
        """Reestablish heap-order property from storage[child] up."""
        while child > 1 and self.less(child//2, child):
            self.swap(child, child//2)
            child = child//2

    def sink(self, parent):
        """Reestablish heap-order property from storage[parent] down."""
        while 2*parent <= self.N:
            child = 2*parent
            if child < self.N and self.less(child, child+1):
                child += 1
            if not self.less(parent, child):
                break
            self.swap(child, parent)

            parent = child

    def peek(self):
        """Peek without disturbing the value at the top of the priority queue."""
        if self.N == 0:
            raise RuntimeError('IndexMinPriorityQueue is empty!')

        return self.values[1]

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        min_value = self.values[1]
        self.values[1] = self.values[self.N]
        self.priorities[1] = self.priorities[self.N]
        self.location[self.values[1]] = 1

        self.values[self.N] = self.priorities[self.N] = None
        self.location.pop(min_value)   # remove from dictionary

        self.N -= 1
        self.sink(1)
        return min_value


def dijkstra_sp(G, src):
    """
    Compute Dijkstra's algorithm using src as source and return dist_to[] with
    results and edge_to[] to be able to recover the shortest paths.
    """
    N = G.number_of_nodes()

    inf = float('inf')
    dist_to = {v:inf for v in G.nodes()}
    dist_to[src] = 0

    impq = IndexedMinPQ(N)
    impq.enqueue(src, dist_to[src])
    for v in G.nodes():
        if v != src:
            impq.enqueue(v, inf)

    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e
            impq.decrease_priority(v, dist_to[v])

    edge_to = {}
    while not impq.is_empty():
        n = impq.dequeue()
        for e in G.edges(n, data=True):
            relax(e)

    return dist_to, edge_to


def dag_trials():
    """Confirm DAG single-source shortest path is O(E+N)."""
    for n in [2**k for k in range(2,7)]:
        dijkstra = 1000*min(timeit.repeat(stmt='dijkstra_sp(dg,1)', setup='''
dg=mesh_graph({})'''.format(n), repeat=20, number=15))/15

        topologic = 1000*min(timeit.repeat(stmt='topological_sp(dg,1)', setup='''
dg=mesh_graph({})'''.format(n), repeat=20, number=15))/15

