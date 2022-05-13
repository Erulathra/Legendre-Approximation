from rich.progress import track

from newton_cotes import newton_cotes_quadrature


def horner_scheme(x, arguments):
    result = arguments[0]
    for a in arguments[1:]:
        result = result * x + a

    return result


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


def legendre_polynomial_arguments(degree: int) -> list[list[float]]:
    arguments = calculate_new_legendre_polynomial_arguments()
    for i in range(degree):
        arguments = calculate_new_legendre_polynomial_arguments(arguments)

    return arguments


def calculate_new_legendre_polynomial_arguments(arguments: list[list[float]] = None) -> [list[list[float]]]:
    if arguments is None:
        return [[1.]]
    if len(arguments) == 1:
        arguments.append([0., 1.])
        return arguments

    degree = len(arguments)
    arguments.append([0. for _ in range(degree + 1)])

    for j in range(1, degree + 1):
        arguments[degree][j] = (2 * degree - 1) / degree * arguments[degree - 1][j - 1]

    for j in range(degree - 1):
        arguments[degree][j] -= (degree - 1) / degree * arguments[degree - 2][j]

    return arguments


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
    for k in track(range(degree), description=f"[green] Obliczanie aproksymacji dla {degree} węzłów"):
        a, b = approximation_range

        legendre_arguments = legendre_polynomial_arguments(degree)

        def function_times_legendre_polynomial(t):
            x = transform_t(t, a, b)
            polynomial_arguments = list(reversed(legendre_arguments[k]))
            return function(x) * horner_scheme(t, polynomial_arguments)

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
