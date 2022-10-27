import numpy as np
import random
import timeit


def counting_sort(lst):
    m = max(lst) + 1
    counts = [0] * m

    for v in lst:
        counts[v] += 1

    pos = 0
    v = 0
    while pos < len(lst):
        for idx in range(counts[v]):
            lst[pos + idx] = v
        pos += counts[v]
        v += 1

    return lst


rand_lst1 = [random.randint(0, 100) for _ in range(50)]
rand_lst2 = [random.randint(0, 100) for _ in range(100)]

r = 10
n = 10**4
reps1 = timeit.repeat(stmt='counting_sort(rand_lst1)', globals=globals(), repeat=r, number=n)
reps2 = timeit.repeat(stmt='counting_sort(rand_lst2)', globals=globals(), repeat=r, number=n)

print(f"counting_sort_1: {np.mean(reps1)}")
print(f"counting_sort_2: {np.mean(reps2)}")
