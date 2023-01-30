def count(A, target):
    """number of times target appears in A"""

    def rcount(lo, hi, target):
        if lo == hi:
            return 1 if A[lo] == target else 0

        mid = (lo+hi)//2
        left = rcount(lo, mid, target)
        right = rcount(mid+1, hi, target)
        return left + right

    return rcount(0, len(A)-1, target)
