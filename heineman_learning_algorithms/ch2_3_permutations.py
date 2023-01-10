from itertools import permutations
from scipy.special import factorial


def factorial_model(n, a):
    return a*factorial(n)


def check_sorted(a):
    for i, val in enumerate(a):
        if i > 0 and val < a[i-1]:
            return False
        return True


def permutation_sort(A):
    for attempt in permutations(A):
        if check_sorted(attempt):
            A[:] = attempt[:]
            return A

