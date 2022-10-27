import random


def tournament_two(A):
    N = len(A)
    winner = [None] * (N-1)
    loser = [None] * (N-1)
    prior = [-1] * (N-1)

    # First round
    idx = 0
    for i in range(0, N, 2):
        if A[i] < A[i+1]:
            winner[idx] = A[i+1]
            loser[idx] = A[i]
        else:
            winner[idx] = A[i]
            loser[idx] = A[i+1]
        idx += 1

    print("\nAfter first round:")
    print("winner:", winner)
    print("loser:", loser)

    # Next rounds
    m = 0
    while idx < N-1:
        if winner[m] < winner[m+1]:
            winner[idx] = winner[m+1]
            loser[idx] = winner[m]
            prior[idx] = m+1
        else:
            winner[idx] = winner[m]
            loser[idx] = winner[m+1]
            prior[idx] = m
        m += 2
        idx += 1

    print("\nAfter next rounds:")
    print("winner:", winner)
    print("loser:", loser)
    print("prior:", prior)

    largest = winner[m]
    second = loser[m]
    while m >= 0:
        if second < loser[m]:
            second = loser[m]
        m = prior[m]

    return largest, second


A = [3, 5, 8, 2]
B = [random.randint(0, 10) for _ in range(10)]

print("A:", A)
tournament_two(A)

print("\nB:", B)
tournament_two(B)
