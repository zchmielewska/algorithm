def num_swaps(A):
    N = len(A)
    seen = [False] * N

    ct = 0
    for i in range(N):
        if not seen[i]:
            idx = i
            num = 0
            while not seen[idx]:
                num += 1
                seen[idx] = True
                idx = A[idx]

            ct += (num - 1)
    return ct

