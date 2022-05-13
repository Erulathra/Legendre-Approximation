from newton_cotes import newton_cotes_quadrature


def legendre_polynomial(x: float, degree: int) -> float:
    if degree == 0:
        return 1
    elif degree == 1:
        return x

    previous_result = 1
    result = x

    for n in range(1, degree):
        new_result = (2 * n + 1) * x * result - n * previous_result
        new_result /= (n + 1)

        previous_result = result
        result = new_result

    return result


def calculate_approximation_polynomial(x: float, a: float, b: float, args: list[float]) -> float:
    result = 0
    for n, argument in enumerate(args):
        result += argument * legendre_polynomial(transform_x(x, a, b), n)

    return result


def legendre_approximation(function,
                           approximation_range: tuple[float, float],
                           degree: int,
                           integral_epsilon: float) -> list[float]:
    result = []
    for k in range(degree):
        a, b = approximation_range

        def function_times_legendre_polynomial(t):
            x = transform_t(t, a, b)
            return function(x) * legendre_polynomial(t, k)

        factor = (2 * k + 1) / 2
        polynomial_factor = factor * newton_cotes_quadrature(function_times_legendre_polynomial, -1, 1,
                                                             integral_epsilon)
        result.append(polynomial_factor)

    return result


# transform t e< -1, 1 > to be in range < a, b >
def transform_t(t, a, b) -> float:
    return ((b - a) * t + (a + b)) / 2


# transform x e< a,b > to be in range < -1, 1 >
def transform_x(x, a, b) -> float:
    return (2 * x - a - b) / (b - a)
