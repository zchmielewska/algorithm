def two_largest_attempt(lst):
    m1 = max(lst[:len(lst) // 2])
    m2 = max(lst[len(lst) // 2:])
    if m1 < m2:
        return m2, m1
    return m1, m2


A = [7, 2, 9, 1, 7, 8, 2, 10]
B = [7, 2, 8, 1, 7, 9, 2, 10]

print("A:", two_largest_attempt(A))
print("B:", two_largest_attempt(B))
