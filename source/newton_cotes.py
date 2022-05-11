from itertools import count

import numpy as np


def simpson_formula(function, a: float, b: float) -> float:
    h = (b - a) / 6.
    return h * (function(a) + 4 * function((a + b) / 2) + function(b))


def newton_cotes_quadrature(function, a: float, b: float, epsilon: float) -> float:
    if a > b:
        b, a = a, b

    previous_result = 0.
    for i in count(1):
        result = 0
        for j in range(i):
            # Calculate subrange size, and add quadrature of this subrange to result
            interpolation_range = abs(a - b) / i
            result += simpson_formula(function, a + interpolation_range * j, a + interpolation_range * (j + 1))

        if abs(result - previous_result) < epsilon:
            return result

        previous_result = result
