def find_max_with_count(A):
    """Count number of comparisons"""
    def frmax(lo, hi):
        if lo == hi:
            return 0, A[lo]

        mid = (lo+hi)//2
        ctleft, left = frmax(lo, mid)
        ctright, right = frmax(mid+1, hi)
        return 1+ctleft+ctright, max(left, right)

    return frmax(0, len(A)-1)

