import pandas as pd


def fragment1(n):
    ct = 0
    for i in range(100):
        for j in range(n):
            for k in range(10000):
                ct += 1
    return ct


def fragment2(n):
    ct = 0
    for i in range(n):
        for j in range(n):
            for k in range(100):
                ct += 1
    return ct


def fragment3(n):
    ct = 0
    for i in range(0, n, 2):
        for j in range(0, n, 2):
            ct += 1
    return ct


def fragment4(n):
    ct = 0
    while n > 1:
        n = n // 2
        ct += 1
    return ct


def fragment5(n):
    ct = 0
    for i in range(2, n, 3):
        for j in range(3, n, 2):
            ct += 1
    return ct


if __name__ == "__main__":
    xs = trials = [2**k for k in range(1, 6)]
    f1 = [fragment1(x) for x in xs]
    f2 = [fragment2(x) for x in xs]
    f3 = [fragment3(x) for x in xs]
    f4 = [fragment4(x) for x in xs]
    f5 = [fragment5(x) for x in xs]

    result = pd.DataFrame({
        "x": xs,
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "f4": f4,
        "f5": f5,
    })

    print(result)
