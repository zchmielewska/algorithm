import timeit


def merge_sort(A):
    aux = [None] * len(A)

    def rsort(lo, hi):
        if hi <= lo:
            return

        mid = (lo+hi)//2
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
                A[i] = aux[left]
                left += 1
            elif aux[right] < aux[left]:
                A[i] = aux[right]
                right += 1
            else:
                A[i] = aux[left]
                left += 1
    rsort(0, len(A)-1)


def slice_merge_sort(A):
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

        i = lo
        j = mid+1

        for k in range(lo, hi+1):
            if i > mid:
                A[k:hi+1] = aux[j:j+hi+1-k]
                return
            if j > hi:
                A[k:hi+1] = aux[i:i+hi+1-k]
                return
            if aux[j]< aux[i]:
                A[k] = aux[j]
                j += 1
            else:
                A[k] = aux[i]
                i += 1

    rsort(0, len(A)-1)


def main():
    max_k = 15

    print("slice merge sort")
    for n in [2**k for k in range(8, max_k)]:
        m_slice = round(1000*min(timeit.repeat(stmt="slice_merge_sort(A)", setup=f"""
import random 
from ch5_4_merge_slice import slice_merge_sort
A=list(range({n}))
random.shuffle(A)""", repeat=10, number=10)))

        m_merge = round(1000*min(timeit.repeat(stmt="merge_sort(A)", setup=f"""
import random 
from ch5_4_merge_slice import merge_sort
A=list(range({n}))
random.shuffle(A)""", repeat=10, number=10)))

        print(n, "m_slice:", m_slice, "m_merge:", m_merge)


if __name__ == "__main__":
    main()
