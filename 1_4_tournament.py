import random


def tournament_two(lst):
    n = len(lst)
    winner = [None] * (n - 1)
    loser = [None] * (n - 1)
    prior = [-1] * (n - 1)

    # First round
    idx = 0
    for i in range(0, n, 2):
        if lst[i] < lst[i + 1]:
            winner[idx] = lst[i + 1]
            loser[idx] = lst[i]
        else:
            winner[idx] = lst[i]
            loser[idx] = lst[i + 1]
        idx += 1

    # Next rounds
    m = 0
    while idx < n-1:
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

    # Is second really the second best?
    largest = winner[m]
    second = loser[m]
    while m >= 0:
        if second < loser[m]:
            second = loser[m]
        m = prior[m]

    return largest, second


A = [3, 5, 8, 2]
B = [random.randint(0, 10) for _ in range(10)]
C = [7, 2, 9, 1, 7, 8, 2, 10]

print("A:", A)
print("winners:", tournament_two(A))
print("\nB:", B)
print("winners:", tournament_two(B))
print("\nC:", C)
print("winners:", tournament_two(C))


def tournament_two_with_odd_participants(lst):
    odd_participant = lst[-1]
    lst = lst[:len(lst)-1]

    n = len(lst)
    winner = [None] * (n - 1)
    loser = [None] * (n - 1)
    prior = [-1] * (n - 1)

    # First round
    idx = 0
    for i in range(0, n, 2):
        if lst[i] < lst[i + 1]:
            winner[idx] = lst[i + 1]
            loser[idx] = lst[i]
        else:
            winner[idx] = lst[i]
            loser[idx] = lst[i + 1]
        idx += 1

    # Next rounds
    m = 0
    while idx < n-1:
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

    # Is second really the second best?
    largest = winner[m]
    second = loser[m]
    while m >= 0:
        if second < loser[m]:
            second = loser[m]
        m = prior[m]

    # Is odd participant better?
    if odd_participant >= largest:
        second = largest
        largest = odd_participant
    elif odd_participant > second:
        second = odd_participant

    return largest, second


D = [3, 5, 8, 2, 7]
E = [7, 2, 9, 1, 7, 8, 2, 10, 1]
F = [3, 5, 8, 2, 10]

print("\nD:", D)
print("winners:", tournament_two_with_odd_participants(D))
print("\nE:", E)
print("winners:", tournament_two_with_odd_participants(E))
print("\nF:", F)
print("winners:", tournament_two_with_odd_participants(F))
