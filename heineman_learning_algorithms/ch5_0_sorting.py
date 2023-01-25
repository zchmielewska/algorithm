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


# Recursion and Divide and Conquer
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


if __name__ == "__main__":
    vals = [5, 3, 4, 10, 2]
    print(selection_sort(vals))

    vals = [5, 3, 4, 10, 2]
    print(insertion_sort(vals))

    vals = [5, 3, 4, 10, 2]
    print(find_max(vals))
