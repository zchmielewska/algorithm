import numpy as np
import random
import timeit


def partition(A, lo, hi, idx):
    """
    Partition using A[idx] as value. Note lo and hi are INCLUSIVE on both
    ends and idx must be valid index. Count the number of comparisons
    by populating A with RecordedItem instances.
    """
    if lo == hi:
        return lo

    A[idx], A[lo] = A[lo], A[idx]  # swap into position
    i = lo
    j = hi + 1
    while True:
        while True:
            i += 1
            if i == hi:
                break
            if A[lo] < A[i]:
                break

        while True:
            j -= 1
            if j == lo:
                break
            if A[j] < A[lo]:
                break

        # doesn't count as comparing two values
        if i >= j:
            break

        A[i], A[j] = A[j], A[i]

    A[lo], A[j] = A[j], A[lo]
    return j


def linear_median(A):
    """
    Efficient implementation that returns median value in arbitrary list,
    assuming A has an odd number of values. Note this algorithm will
    rearrange values in A.
    """
#     if len(A) % 2 == 0:
#         raise ValueError('linear_median() only coded to work with odd number of values.')
    lo = 0
    hi = len(A) - 1
    mid = hi // 2
    while lo < hi:
        idx = random.randint(lo, hi)     # select valid index randomly
        j = partition(A, lo, hi, idx)

        if j == mid:
            return A[j]
        if j < mid:
            lo = j+1
        else:
            hi = j-1
    return A[lo]


def median(lst):
    lst = sorted(lst)
    return lst[len(lst)//2]


r = 10
n = 10**5
A = [random.randint(1, 100) for _ in range(9)]
reps1 = timeit.repeat(stmt='linear_median(A)', globals=globals(), repeat=r, number=n)
reps2 = timeit.repeat(stmt='median(A)', globals=globals(), repeat=r, number=n)

print(f"linear_median: {np.mean(reps1)}")
print(f"median: {np.mean(reps2)}")

