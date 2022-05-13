import random
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

        # generate interpolation nodes
        interpolation_range = abs(a - b) / i
        interpolation_nodes: list[float] = [node for node in np.arange(a, b, interpolation_range)]
        interpolation_nodes.append(b)

        # generate noise inside range
        for j in range(1, len(interpolation_nodes) - 1):
            noise = interpolation_range * 0.6
            interpolation_nodes[j] += random.randint(-100, 100) / 100 * noise

        for first_node, second_node in zip(interpolation_nodes, interpolation_nodes[1:]):
            result += simpson_formula(function, first_node, second_node)

        if abs(result - previous_result) < epsilon:
            return result

        previous_result = result
