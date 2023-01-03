import numpy as np
import pandas as pd

from functools import partial
from scipy.optimize import curve_fit


def f4(n):
    ct = 1
    while n >= 2:
        ct += 1
        n = n ** 0.5
    return ct


def log_log_model(n, a):
    return a * np.log2(np.log2(n))


if __name__ == "__main__":
    xs = [2**k for k in range(1, 51)]
    ys = [f4(x) for x in xs]
    [(a), _] = curve_fit(log_log_model, np.array(xs), np.array(ys))
    predict = partial(log_log_model, a=a)
    predictions = [predict(x) for x in xs]

    result = pd.DataFrame({
        "xs": xs,
        "ys": ys,
        "predicitons": predictions
    })

    print(result)


