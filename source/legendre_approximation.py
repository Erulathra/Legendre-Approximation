from newton_cotes import newton_cotes_quadrature


def legendre_polynomial(x: float, degree: int) -> float:
    previous_result = 1
    result = x

    if degree == 0:
        return previous_result
    elif degree == 1:
        return result

    for n in range(1, degree):
        new_result = (2 * n + 1) * x * result - n * previous_result
        new_result /= (n + 1)

        previous_result = result
        result = new_result

    return result


def calculate_approximation_polynomial(x: float, args: list[float]) -> float:
    result = 0
    for n, argument in enumerate(args):
        result += argument * legendre_polynomial(x, n)

    return result


def legendre_approximation(function,
                           approximation_range: tuple[float, float],
                           degree: int,
                           integral_epsilon: float) -> list[float]:
    result = []
    for k in range(degree):
        a, b = approximation_range

        def function_times_legendre_polynomial(x):
            new_x = transform_x(x, a, b)
            return function(new_x) * legendre_polynomial(x, k)

        def square_legendre_polynomial(x):
            result = legendre_polynomial(x, k)
            return result * result

        polynomial_factor = newton_cotes_quadrature(function_times_legendre_polynomial, -1, 1, integral_epsilon)
        polynomial_factor /= newton_cotes_quadrature(square_legendre_polynomial, -1, 1, integral_epsilon)
        result.append(polynomial_factor)

    return result


def transform_x(x, a, b) -> float:
    return (2 * x - a - b) / (b - a)
