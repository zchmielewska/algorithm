# Selection Sort (Sortowanie przez wybieranie)
def selection_sort(A):
    N = len(A)
    for i in range(N-1):
        min_index = i
        for j in range(i+1, N):
            if A[j] < A[min_index]:
                min_index = j
        A[i], A[min_index] = A[min_index], A[i]
    return A


# Insertion Sort (Sortowanie przez wstawianie)
def insertion_sort(A):
    N = len(A)
    for i in range(1, N):
        for j in range(i, 0, -1):
            if A[j-1] <= A[j]:
                break
            A[j], A[j-1] = A[j-1], A[j]
    return A


# Recursion and Divide and Conquer (Rekourencja oraz podejście dziel i rządź)
def fact(N):
    if N <= 1:
        return 1
    return N * fact(N-1)


def find_max(A):
    def rmax(lo, hi):
        if lo == hi:
            return A[lo]
        mid = (lo+hi)//2
        L = rmax(lo, mid)
        R = rmax(mid+1, hi)
        return max(L, R)
    return rmax(0, len(A)-1)


# Recursive merge sort (Sortowanie przez scalanie)
def merge_sort(A):
    aux = [None] * len(A)

    def rsort(lo, hi):
        if hi <= lo:
            return

        mid = (lo+hi) // 2
        rsort(lo, mid)
        rsort(mid+1, hi)
        merge(lo, mid, hi)

    def merge(lo, mid, hi):
        aux[lo:hi+1] = A[lo:hi+1]

        left = lo
        right = mid+1

        for i in range(lo, hi+1):
            if left > mid:
                A[i] = aux[right]
                right += 1
            elif right > hi:
                A[i] = aux[right]
                pass
            # TO BE FINISHED

    rsort(0, len(A)-1)


# Quick sort (Sortowanie szybkie)
def partition(A, lo, hi, idx):
    """
    Partition using A[idx] as value. Note lo and hi are INCLUSIVE on both
    ends and idx must be valid index. Count the number of comparisons
    by populating A with RecordedItem instances.
    """
    if lo == hi:
        return lo

    A[idx],A[lo] = A[lo],A[idx]    # swap into position
    i = lo
    j = hi + 1
    while True:
        while True:
            i += 1
            if i == hi: break
            if A[lo] < A[i]: break

        while True:
            j -= 1
            if j == lo: break
            if A[j] < A[lo]: break

        # doesn't count as comparing two values
        if i >= j: break

        A[i],A[j] = A[j],A[i]

    A[lo],A[j] = A[j],A[lo]
    return j


def quick_sort(A):
    def qsort(lo, hi):
        if hi <= lo:
            return

        pivot_idx = lo
        location = partition(A, lo, hi, pivot_idx)

        qsort(lo, location-1)
        qsort(location+1, hi)

    qsort(0, len(A)-1)


# Heap sort (Sortowanie przez kopcowanie)
class HeapSort:
    def __init__(self, A):
        self.A = A
        self.N = len(A)

        for k in range(self.N//2, 0, -1):
            self.sink(k)

    def sort(self):
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)

    def less(self, i, j):
        return self.A[i-1] < self.A[j-1]

    def swap(self, i, j):
        self.A[i-1], self.A[j-1] = self.A[j-1], self.A[i-1]


# Tim Sort
def tim_sort(A):
    N = len(A)
    if N < 64:
        insertion_sort(A, 0, N-1)
        return

    size = compute_min_run(N)
    for lo in range(0, N, size):
        insertion_sort(A, lo, min(lo+size-1, N-1))

    aux = [None]*N
    while size < N:
        for lo in range(0, N, 2*size):
            mid = min(lo + size - 1, N-1)
            hi = min(lo + 2*size - 1, N-1)
            merge(A, lo, mid, hi, aux)

        size = 2 * size


if __name__ == "__main__":
    vals = [5, 3, 4, 10, 2]
    print(selection_sort(vals))

    vals = [5, 3, 4, 10, 2]
    print(insertion_sort(vals))

    vals = [5, 3, 4, 10, 2]
    print(find_max(vals))
