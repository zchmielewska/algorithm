def recursive_two(A):
    """Return two largest values in a list."""

    def rtwo(lo, hi):
        # Base cases: one or two values
        if lo == hi:
            return (A[lo], None)

        if lo+1 == hi:
            if A[lo] < A[hi]:
                return (A[hi], A[lo])
            return (A[lo], A[hi])

        mid = (lo+hi)//2
        L = rtwo(lo, mid)
        R = rtwo(mid+1, hi)

        if L[0] < R[0]:
            if R[1] is None:
                return (R[0], L[0])
            return (R[0], R[1]) if L[0] < R[1] else (R[0], L[0])
        return (L[0], L[1]) if R[0] < L[1] else (L[0], R[0])

    return rtwo(0, len(A)-1)


if __name__ == "__main__":
    lst = [3, 2, 8, 4, 9, 1, 4]
    result = recursive_two(lst)
    print(result)

