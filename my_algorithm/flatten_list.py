import numpy as np
import timeit
import random
import functools
import operator
import itertools


lst = [[1, 2, 3], [4, 5], [7]]


def flatten1(lst):
    flat_list = []
    for sublist in lst:
        for item in sublist:
            flat_list.append(item)

    return flat_list

print("flatten1:", flatten1(lst))


def flatten2(lst):
    return [item for sublist in lst for item in sublist]


print("flatten2:", flatten2(lst))


def flatten3(lst):
    return functools.reduce(operator.iconcat, lst, [])


print("flatten3:", flatten3(lst))


def flatten4(lst):
    return list(itertools.chain(*lst))


print("flatten4:", flatten4(lst))


def flatten5(lst):
    return list(np.concatenate(lst).flat)


print("flatten5:", flatten5(lst))


def flatten6(lst):
    return sum(lst, [])


print("flatten6:", flatten6(lst))


x = [[random.random() for _ in range(1000)], [random.random() for _ in range(1000)], [random.random() for _ in range(1000)]]

r = 10
n = 10**4
reps1 = timeit.repeat(stmt='flatten1(x)', globals=globals(), repeat=r, number=n)
reps2 = timeit.repeat(stmt='flatten2(x)', globals=globals(), repeat=r, number=n)
reps3 = timeit.repeat(stmt='flatten3(x)', globals=globals(), repeat=r, number=n)
reps4 = timeit.repeat(stmt='flatten4(x)', globals=globals(), repeat=r, number=n)
reps5 = timeit.repeat(stmt='flatten5(x)', globals=globals(), repeat=r, number=n)
reps6 = timeit.repeat(stmt='flatten6(x)', globals=globals(), repeat=r, number=n)

print("r=", r, "n=", n)
print(f"flatten1(): {np.mean(reps1)}")
print(f"flatten2(): {np.mean(reps2)}")
print(f"flatten3(): {np.mean(reps3)}")
print(f"flatten4(): {np.mean(reps4)}")
print(f"flatten5(): {np.mean(reps5)}")
print(f"flatten6(): {np.mean(reps6)}")

#  Results:
# flatten1: [1, 2, 3, 4, 5, 7]
# flatten2: [1, 2, 3, 4, 5, 7]
# flatten3: [1, 2, 3, 4, 5, 7]
# flatten4: [1, 2, 3, 4, 5, 7]
# flatten5: [1, 2, 3, 4, 5, 7]
# flatten6: [1, 2, 3, 4, 5, 7]
# r= 10 n= 10000
# flatten1(): 2.35734534
# flatten2(): 1.2080104799999993
# flatten3(): 0.15313860999999845
# flatten4(): 0.42333723999999934
# flatten5(): 4.00048718
# flatten6(): 0.22301624999999917
# Thoughts: flatten3 is the best but flatten6 is also very good and doesn't require any packages