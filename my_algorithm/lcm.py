# LCM = Least Common Multiple - the smallest multiple that is divisible by both numbers

import math
from functools import reduce


def lcm(*args):
    return reduce(lambda a, b: abs(a*b) // math.gcd(a, b), args)


print(lcm(12, 15, 20))  # Output: 60
