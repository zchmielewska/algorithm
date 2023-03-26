import random
import networkx as nx


class Maze:
    """
    Construct a random maze whose entrance is at the middle of the top row
    of the rectangular maze, and the exit is at the middle of the bottom
    row.

    The basic technique is to assemble a maze where every cell has intact walls,
    and then conduct a depth-first-search through the maze, tearing down walls
    when heading into a new, unvisited cell.

    To add a bit of variety, a salt parameter randomly clears additional walls,
    with a default setting of 0.05. If you salt=0, then the maze will have
    perfectly cut rooms, with a long and winding solution to the maze.

    This implementation uses stack-based Depth First Search to handle cases
    with large mazes.
    """
    def __init__(self, num_rows, num_cols, salt=0.05):
        """initialize maze"""

        if salt < 0 or salt > 1:
            raise ValueError('salt parameter must be a floating point between 0 and 1 inclusive.')

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.salt = salt
        self.construct()

    def start(self):
        """Starting cell for maze."""
        return (0, self.num_cols//2)

    def end(self):
        """Ending cell for maze."""
        return (self.num_rows-1, self.num_cols//2)

    def clear_wall(self, from_cell, to_cell):
        """Remove wall between two cells"""
        if from_cell[1] == to_cell[1]:
            self.south_wall[min(from_cell[0],to_cell[0]),from_cell[1]] = False
        else:
            self.east_wall[from_cell[0], min(from_cell[1], to_cell[1])] = False

    def clear_all_walls(self, in_cell):
        """Clear all walls for cell as part of attempt to open more solutions."""
        if 0 < in_cell[0] < self.num_rows-1:
            self.south_wall[in_cell[0], in_cell[1]] = False
        if 0 < in_cell[1] < self.num_cols-1:
            self.east_wall[in_cell[0], in_cell[1]] = False

        if 0 < in_cell[1] < self.num_cols-1:
            self.east_wall[in_cell[0], in_cell[1]-1] = False
        if 0 < in_cell[0] < self.num_rows-1:
            self.south_wall[in_cell[0]-1, in_cell[1]] = False

    def dfs_visit_nr(self, sq):
        """conduct non-recursive DFS search to build maze"""
        path = [sq]
        self.marked[sq] = True

        while len(path) > 0:
            sq = path[0]
            more = self.neighbors[sq]
            if len(more) > 0:
                cell = random.choice(self.neighbors[sq])
                self.neighbors[sq].remove(cell)
                if not self.marked[cell]:
                    self.clear_wall(sq, cell)
                    if random.random() < self.salt:
                        self.clear_all_walls(sq)
                    path.insert(0, cell)
                    self.marked[cell] = True
            else:
                self.marked[sq] = True
                del path[0]

    def initialize(self):
        """Reset to initial state with no walls and all neighbors are set."""
        self.marked     = dict( ((r,c), False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.east_wall  = dict( ((r,c), False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.south_wall = dict( ((r,c), False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.neighbors  = dict( ((r,c), [])    for r in range(self.num_rows) for c in range(self.num_cols) )

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.east_wall[r,c] = True
                self.south_wall[r,c] = True

                if r != 0:
                    self.neighbors[r,c].append((r-1,c))
                if r != self.num_rows-1:
                    self.neighbors[r,c].append((r+1,c))

                if c != 0:
                    self.neighbors[r,c].append((r,c-1))
                if c != self.num_cols-1:
                    self.neighbors[r,c].append((r,c+1))

    def construct(self):
        """construct maze of given height/width and size."""
        self.initialize()
        sq = self.start()
        self.dfs_visit_nr(sq)
        self.south_wall[self.end()] = False


class Entry:
    """Represents a (v,p) entry in a priority queue."""
    def __init__(self, v, p):
        self.value = v
        self.priority = p

    def __str__(self):
        return '[{} p={}]'.format(self.value, self.priority)


class Node:
    """
    Node structure to use in linked list.
    """
    def __init__(self, val, rest=None):
        self.value = val
        self.next = rest

    def __str__(self):
        return '[{}]'.format(self.value)

    def __iter__(self):
        """
        Generator to retrieve values in linked list in order.

        Enabled Python code like following, where alist is a Node.

            for v in alist:
                print(v)

        """
        yield self.value

        if self.next:
            for v in self.next:
                yield v


class Stack:
    """
    Implementation of a Stack using linked lists.
    """
    def __init__(self):
        self.top = None

    def is_empty(self):
        """Determine if queue is empty."""
        return self.top is None

    def push(self, val):
        """Push new item to the top of the stack."""
        self.top = Node(val, self.top)

    def pop(self):
        """Remove and return top item from stack."""
        if self.is_empty():
            raise RuntimeError('Stack is empty')

        val = self.top.value
        self.top = self.top.next
        return val


class Queue:
    """
    Implementation of a Queue using linked lists.
    """
    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        """Determine if queue is empty."""
        return self.first is None

    def enqueue(self, val):
        """Enqueue new item to end of queue."""
        if self.first is None:
            self.first = self.last = Node(val)
        else:
            self.last.next = Node(val)
            self.last = self.last.next

    def dequeue(self):
        """Remove and return first item from queue."""
        if self.is_empty():
            raise RuntimeError('Queue is empty')

        val = self.first.value
        self.first = self.first.next
        return val


class PQ:
    """
    Heap storage for a priority queue.
    """
    def __init__(self, size):
        self.size = size
        self.storage = [None] * (size+1)
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

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
        self.storage[self.N] = Entry(v, p)
        self.swim(self.N)

    def less(self, i, j):
        """
        Helper function to determine if storage[j] has higher
        priority than storage[i].
        """
        return self.storage[i].priority < self.storage[j].priority

    def swap(self, i, j):
        """Switch the values in storage[i] and storage[j]."""
        self.storage[i],self.storage[j] = self.storage[j],self.storage[i]

    def swim(self, child):
        """Reestablish heap-order property from storage[child] up."""
        while child > 1 and self.less(child//2, child):
            self.swap(child, child//2)
            child = child // 2

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
        """
        Peek without disturbing the value at the top of the priority queue. Must
        return entire Entry, since the one calling might like to know priority and value
        """
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        return self.storage[1]

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        max_entry = self.storage[1]
        self.storage[1] = self.storage[self.N]
        self.storage[self.N] = None
        self.N -= 1
        self.sink(1)
        return max_entry.value


def distance_to(from_cell, to_cell):
    return abs(from_cell[0] - to_cell[0]) + abs(from_cell[1] - to_cell[1])


def to_networkx(maze):
    G = nx.Graph()

    for r in range(maze.num_rows):
        for c in range(maze.num_cols):
            G.add_node((r, c), pos=(c, maze.num_rows - r))

    for r in range(maze.num_rows):
        for c in range(maze.num_cols):
            if not maze.south_wall[r, c] and r < maze.num_rows -1:
                G.add_edge((r, c), (r+1, c))
            if not maze.east_wall[r,c]:
                G.add_edge((r, c), (r, c+1))
    return G


def annotated_dfs_search(G, src, target):
    """
    Apply non-recursive Depth First Search to a graph from src. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.
    """
    marked = {}
    node_from = {}

    stack = Stack()
    marked[src] = True
    stack.push(src)

    while not stack.is_empty():
        v = stack.pop()
        if v == target:
            return len(marked)

        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                stack.push(w)

    return len(marked)


def annotated_bfs_search(G, src, target):
    """
    Apply Depth First Search to a graph from a starting node. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.
    """
    marked = {}
    node_from = {}

    q = Queue()
    marked[src] = True
    q.enqueue(src)

    while not q.is_empty():
        v = q.dequeue()
        if v == target:
            return len(marked)

        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                q.enqueue(w)

    return len(marked)


def annotated_guided_search(G, src, target, distance):
    """
    Non-recursive depth-first search investigating given position. Needs
    a distance (node1, node2) function to determine distance between two nodes.

    Performance is O(N log N + E) since every edge is visited once for a directed
    graph and twice for an undirected graph. Each of the N nodes is processed by
    the priority queue, where dequeue() and enqueue() operations are each O(log N).
    While it is unlikely that the priority queue will ever contain N nodes, the
    worst case possibility always exists.
    """
    marked = {}
    node_from = {}

    pq = PQ(G.number_of_nodes())
    marked[src] = True

    # Using a MAX PRIORITY QUEUE means we rely on negative distance to
    # choose the one that is closest...
    pq.enqueue(src, -distance(src, target))

    while not pq.is_empty():
        v = pq.dequeue()
        if v == target:
            return len(marked)

        for w in G.neighbors(v):
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                pq.enqueue(w, -distance(w, target))

    return len(marked)


def maze_to_defeat_guided_search(n=15):
    """
    Construct maze that defeats guided search by forcing exploration of (n-1)^2 + n/2
    cells when n is even. For odd n, it becomes (n-1)^2 + n/2 + 1.
    """
    m = Maze(n,n)
    m.initialize()                     # back to scratch WITH ALL WALLS

    for r in range(0, m.num_rows-2):   # leave open the first and last
        for c in range(0, m.num_cols):
            m.south_wall[(r,c)] = False
    m.south_wall[(m.num_rows-2,0)] = False
    m.south_wall[(m.num_rows-2,m.num_cols-1)] = False
    m.east_wall[(m.num_rows-1,0)] = False
    m.east_wall[(m.num_rows-1,m.num_cols-2)] = False
    m.east_wall[(0,0)] = False
    m.east_wall[(0,m.num_cols-2)] = False

    for r in range(0, m.num_rows):   # leave open the first and last
        for c in range(1, m.num_cols-2):
            m.east_wall[(r,c)] = False

    return m


def search_trials():
    for N in [4, 8, 16, 32, 64, 128]:
        num_bfs = 0
        num_dfs = 0
        num_gs = 0
        for i in range(512):
            random.seed(i)
            m = Maze(N,N)
            G = to_networkx(m)

            num_bfs += annotated_bfs_search(G, m.start(), m.end())
            num_dfs += annotated_dfs_search(G, m.start(), m.end())
            num_gs += annotated_guided_search(G, m.start(), m.end(), distance_to)

    for N in [4, 8, 16, 32, 64, 128]:
        m = maze_to_defeat_guided_search(N)
        G = to_networkx(m)

        num_bfs = annotated_bfs_search(G, m.start(), m.end())
        num_dfs = annotated_dfs_search(G, m.start(), m.end())
        num_gs = annotated_guided_search(G, m.start(), m.end(), distance_to)
