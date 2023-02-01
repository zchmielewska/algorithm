import timeit


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-2) + fibonacci(n-1)


def lucas(n):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return lucas(n-2) + lucas(n-1)


def fib_with_lucas(n):
    """F_(i+j) = (F_i * L_j) + (F_j * L_i) / 2"""
    if n == 0:
        return 0

    if n <= 2:
        return 1

    if n == 3:
        return 2

    i = n//2
    j = n - i
    return ((fib_with_lucas(i) * lucas_with_fib(j)) + (fib_with_lucas(j) * lucas_with_fib(i))) / 2


def lucas_with_fib(n):
    if n == 0:
        return 2

    if n == 1:
        return 1

    return fib_with_lucas(n-1) + fib_with_lucas(n+1)


if __name__ == "__main__":
    n = 35
    fib_time = timeit.timeit(
        stmt=f"fibonacci({n})",
        setup="from ch5_6_fibonacci_and_lucas import fibonacci",
        number=1)
    print(f"Fibonacci for {n} elements:", fib_time)

    luc_time = timeit.timeit(
        stmt=f"lucas({n})",
        setup="from ch5_6_fibonacci_and_lucas import lucas",
        number=1)
    print(f"Lucas for {n} elements:", luc_time)

    fib_with_luc_time = timeit.timeit(
        stmt=f"fib_with_lucas({n})",
        setup="from ch5_6_fibonacci_and_lucas import fib_with_lucas",
        number=1)
    print(f"Fibonacci with Lucas for {n} elements:", fib_with_luc_time)

