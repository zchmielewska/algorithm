import matplotlib.pyplot as plt
from resources.highway import highway_map

WEIGHT = "weight"


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


def edges_path_to(edge_to, src, target):
    """Recover path from src to target."""
    if not target in edge_to:
        raise ValueError('{} is unreachable from {}'.format(target, src))

    path = []
    v = target
    while v != src:
        path.append(v)
        v = edge_to[v][0]

    # last one to push is the source, which makes it
    # the first one to be retrieved
    path.append(src)
    path.reverse()
    return path


def tmg_load(raw_data):
    """
    Load up a TMG 1.0 simple file into a directed weighted graph, using
    long/lat coordinate calculator for distance.

        TMG 1.0 simple
        #N #E
        {NODE: LABEL LAT LONG}
        {EDGE: id1 id2 LABEL}

    For each edge, compute the distance. Also return labels for the nodes.
    """
    G = nx.Graph()
    line = 0
    if not 'TMG' in raw_data[line]:
        raise ValueError('Contents is not a valid TMG file ({}).'.format(raw_data[line]))
    line += 1

    (snum_nodes, snum_edges) = raw_data[line].split()
    line += 1
    num_nodes = int(snum_nodes)
    num_edges = int(snum_edges)

    positions = {}
    labels = {}

    for i in range(num_nodes):
        (label, slat1, slong1) = raw_data[line].split()
        line += 1

        positions[i] = (float(slat1), float(slong1))
        labels[i] = label
        G.add_node(i)

    for i in range(num_edges):
        (su, sv, _) = raw_data[line].split()
        line += 1

        u = int(su)
        v = int(sv)
        d = distance(positions[u], positions[v])
        G.add_edge(u, v, weight=d)

    return G, positions, labels


def compute_distance(positions, node_from, src, target):
    """
    Compute total distance from src to target, traversing positions and using
    positions[] information as waypoints for distance.
    """
    total = 0
    last_pos = None
    v = target
    while v != src:
        pos = positions[v]
        v = node_from[v]
        if last_pos:
            total += distance(pos, last_pos)
        last_pos = pos
    total += distance(positions[src], last_pos)
    return total


def plot_gps(positions, s=8, marker='.', color='blue'):
    """Draw positions of individual nodes."""
    import matplotlib.pyplot as plt

    x = []
    y = []
    for i in positions:
        pos = positions[i]
        x.append(pos[1])
        y.append(pos[0])
    plt.scatter(x, y, marker=marker, s=s, color=color)

def bounding_ids(positions):
    """Compute the distant borders via GPS in the positions. [NORTH, EAST, SOUTH, WEST]."""
    north = -360
    east  = -360
    south = 360
    west  = 360
    north_id = -1
    east_id = -1
    south_id = -1
    west_id = -1

    for node in positions:
        gps = positions[node]
        if gps[0] > north:
            north = gps[0]
            north_id = node
        if gps[0] < south:
            south = gps[0]
            south_id = node
        if gps[1] > east:
            east = gps[1]
            east_id = node
        if gps[1] < west:
            west = gps[1]
            west_id = node
    return north_id, east_id, south_id, west_id


def plot_highways(positions, edges, color='gray'):
    """Plot highways with linesegments."""
    for e in edges:
        head = positions[e[0]]
        tail = positions[e[1]]
        plt.plot([head[1], tail[1]],[head[0], tail[0]], linewidth=1, color=color)


def distance(gps1, gps2):
    """
    Return reasonably distance in miles. Based on helpful method found here:

    https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    """
    (lat1, long1) = gps1
    (lat2, long2) = gps2

    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((long2-long1)*p))/2
    return 7917.509282 * asin(sqrt(a))    # convert into miles and use 12742 as earth diameter in KM


"""
Supporting functions for plotting the latitude/longitude data.
"""

from ch07.dependencies import plt_error
from ch07.replacement import WEIGHT

def plot_edge_path(positions, src, target, edge_to, marker='.', color='green'):
    """
    Plot path using list of nodes in edge_to[] according to positional information
    in positions.
    """
    if plt_error:
        return
    import matplotlib.pyplot as plt

    nodex = []
    nodey = []
    e = edge_to[target]
    my_total = 0
    while e[0] != src:
        pos = positions[e[0]]
        nodex.append(pos[1])
        nodey.append(pos[0])
        my_total += e[2][WEIGHT]
        e = edge_to[e[0]]
    my_total += e[2][WEIGHT]
    print('my total={}'.format(my_total))
    plt.plot(nodex, nodey, color=color)
    plt.scatter(nodex, nodey, marker=marker, color=color)

def plot_path(positions, path, marker='.', color='red'):
    """
    Plot path using list of nodes in path[] according to positional information
    in positions.
    """
    if plt_error:
        return
    import matplotlib.pyplot as plt

    pxs = []
    pys = []
    for v in path:
        pos = positions[v]
        pxs.append(pos[1])
        pys.append(pos[0])
    plt.plot(pxs, pys, color=color)
    plt.scatter(pxs, pys, marker=marker, color=color)

def plot_node_from(positions, src, target, node_from, marker='.', color='orange'):
    """Plot path from src to target using node_from[] information."""
    if plt_error:
        return
    import matplotlib.pyplot as plt

    nodex = []
    nodey = []
    v = target
    while v != src:
        pos = positions[v]
        nodex.append(pos[1])
        nodey.append(pos[0])
        v = node_from[v]
    pos = positions[src]
    nodex.append(pos[1])
    nodey.append(pos[0])
    plt.plot(nodex, nodey, color=color)
    plt.scatter(nodex, nodey, marker=marker, color=color)

"""
Provide access to where images are output.
"""
import os

IMAGE_DIR = 'images'

def visualize(tbl, description, label, xaxis='Problem instance size', yaxis='Time (in seconds)'):
    """
    Plot the table and store into file. If MatPlotLib is not installed, this
    silently ignores this request.
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except ImportError:
        return

    # make sure interactive is off....
    plt.ioff()

    # Grab x values from the first label in headers
    x_arr = np.array(tbl.column(tbl.labels[0]))
    fig, axes = plt.subplots()

    # It may be that some of these columns are PARTIAL; if so, truncate xs as well
    for hdr in tbl.labels[1:]:
        yvals = np.array(tbl.column(hdr))
        xvals = x_arr[:]
        if len(yvals) < len(xvals):
            xvals = xvals[:len(yvals)]

        axes.plot(xvals, yvals, label=hdr)

    axes.set(xlabel=xaxis, ylabel=yaxis, title=description)
    axes.legend(loc='upper left')
    axes.grid()

    img_file = image_file(label)
    fig.savefig(img_file)
    print('Wrote image to', img_file)
    print()

def image_file(relative_name):
    """
    Return file location where image directory is found, using relative_name.
    If directory does not exist, then just place in current directory.
    """
    # If directory exists, then return
    if os.path.isdir(IMAGE_DIR):
        return ''.join([IMAGE_DIR, os.sep, relative_name])

    if os.path.isdir(''.join(['..', os.sep, IMAGE_DIR])):
        return ''.join(['..', os.sep, IMAGE_DIR, os.sep, relative_name])

    return ''.join(['.',os.sep,relative_name])

def avoid_interstate_90():
    """Find shortest path from westernmost-MA to easternmost-MA that avoids I-90."""
    (G,positions,labels) = tmg_load(highway_map())

    # Since graph is undirected, we will visit each edge twice. Make sure to
    # only remove when u < v to avoid deleting same edge twice
    edges_to_remove = []
    destination = None
    for u in G.nodes():
        if labels[u] == 'I-90@134&I-93@20&MA3@20(93)&US1@I-93(20)':       # SPECIAL LABEL in BOSTON
            destination = u
        for v in G.adj[u]:
            if 'I-90' in labels[u] and 'I-90' in labels[v] and u < v:
                edges_to_remove.append((u,v))

    (_,_,_,WEST) = bounding_ids(positions)
    (dist_to, edge_to) = dijkstra_sp(G, WEST)
    print('Original Dijkstra shortest distance is {} total steps with distance={:.1f}'.format(len(edges_path_to(edge_to, WEST, destination))-1, dist_to[destination]))

    print('num edges:', G.number_of_edges())
    for e in edges_to_remove:
        G.remove_edge(e[0], e[1])
    print('num edges:', G.number_of_edges())

    # create a new graph whose edges are not wholly on I-90
    (_,_,_,WEST) = bounding_ids(positions)
    (dist_to, edge_to) = dijkstra_sp(G, WEST)
    print('Dijkstra shortest distance avoiding I-90 is {} total steps with distance={:.1f}'.format(len(edges_path_to(edge_to, WEST, destination))-1, dist_to[destination]))
    path = edges_path_to(edge_to,WEST, destination)
    plt.clf()
    plot_gps(positions)
    plot_highways(positions, G.edges())
    plot_path(positions, path)

    output_file = image_file('figure-mass-no-I-90-dijkstra.svg')
    plt.savefig(output_file, format="svg")
    print(output_file)
    plt.clf()
    return output_file