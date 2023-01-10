import numpy as np
import timeit


def is_palindrome1(w):
    return w[::-1] == w


def is_palindrome2(w):
    while len(w) > 1:
        if w[0] != w[-1]:
            return False
        w = w[1:-1]


def is_palindrome3(w):
    for i in range(len(w) // 2):
        if w[i] != w[-(i+1)]:
            return False
    return True


def is_palindrome4(w):
    return w[0:len(w)//2] == w[len(w):len(w)//2:-1]


word = "kajak"
r = 10
n = 10**6
reps1 = timeit.repeat(stmt='is_palindrome1(word)', globals=globals(), repeat=r, number=n)
reps2 = timeit.repeat(stmt='is_palindrome2(word)', globals=globals(), repeat=r, number=n)
reps3 = timeit.repeat(stmt='is_palindrome3(word)', globals=globals(), repeat=r, number=n)
reps4 = timeit.repeat(stmt='is_palindrome4(word)', globals=globals(), repeat=r, number=n)

print(f"is_palindrome1: {np.mean(reps1)}")
print(f"is_palindrome2: {np.mean(reps2)}")
print(f"is_palindrome3: {np.mean(reps3)}")
print(f"is_palindrome4: {np.mean(reps4)}")

