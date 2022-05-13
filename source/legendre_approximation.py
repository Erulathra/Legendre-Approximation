from itertools import count

from rich.progress import track

from newton_cotes import newton_cotes_quadrature


def horner_scheme(x, arguments):
    result = arguments[0]
    for a in arguments[1:]:
        result = result * x + a

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


def calculate_approximation_polynomial(x: float,
                                       approximation_range: tuple[float, float],
                                       args: list[float],
                                       legendre_arguments: list[list[float]]) -> float:
    result = 0
    a, b = approximation_range
    for n, argument in enumerate(args):
        polynomial_arguments = list(reversed(legendre_arguments[n]))
        result += argument * horner_scheme(transform_x(x, a, b), polynomial_arguments)

    return result


def legendre_approximation(function,
                           approximation_range: tuple[float, float],
                           epsilon: float,
                           cotes_epsilon: float,
                           error_epsilon: float = 0.001) -> list[float]:
    legendre_arguments = legendre_polynomial_arguments(0)

    for i in count(0):
        result = calculate_legendre_approximation(function, approximation_range, legendre_arguments, cotes_epsilon)

        # calculate error
        def approximation_polynomial(x): return calculate_approximation_polynomial(x, approximation_range, result, legendre_arguments)
        error = approximation_error(function, approximation_polynomial, approximation_range, error_epsilon)

        print(f"Błąd approksymacji: {error}")

        if error < epsilon:
            return result

        legendre_arguments = calculate_new_legendre_polynomial_arguments(legendre_arguments)


def calculate_legendre_approximation(function,
                                     approximation_range: tuple[float, float],
                                     legendre_arguments: list[list[float]],
                                     cotes_epsilon: float) -> list[float]:
    result = []
    degree = len(legendre_arguments)
    for k in track(range(degree), description=f"[green] Obliczanie aproksymacji dla {degree} węzłów"):
        a, b = approximation_range

        def function_times_legendre_polynomial(t):
            x = transform_t(t, a, b)
            polynomial_arguments = list(reversed(legendre_arguments[k]))
            return function(x) * horner_scheme(t, polynomial_arguments)

        factor = (2 * k + 1) / 2
        polynomial_factor = factor * newton_cotes_quadrature(function_times_legendre_polynomial, -1, 1, cotes_epsilon)
        result.append(polynomial_factor)

    return result


# transform t e< -1, 1 > to be in range < a, b >
def transform_t(t, a, b) -> float:
    return ((b - a) * t + (a + b)) / 2


# transform x e< a,b > to be in range < -1, 1 >
def transform_x(x, a, b) -> float:
    return (2 * x - a - b) / (b - a)


def approximation_error(func, approximation, approximation_range, cotes_epsilon):
    def integral_func(x): return abs(func(x) - approximation(x))

    a, b = approximation_range
    return newton_cotes_quadrature(integral_func, a, b, cotes_epsilon)
