import math

from rich import print

import legendre_approximation as la
from charts import Plot

functions = (lambda x: 0.7 * math.fabs(x),
             lambda x: 2 ** (math.cos(x)),
             lambda x: x ** 3 - 2 * x + 4 * x - 10,
             lambda x: math.sin(x),
             lambda x: math.sin(1/x) if x != 0 else 0)


def main():
    func = functions[4]
    a, b = (-3, 5)
    # len_args = la.legendre_polynomial_arguments(100)
    # args = la.calculate_legendre_approximation(func, (a, b), len_args, 0.00001)
    args = la.legendre_approximation(func, (a, b), 0.5, 0.00001, 0.01)
    print(args)

    len_args = la.legendre_polynomial_arguments(len(args))
    def approximation_polynomial(x): return la.calculate_approximation_polynomial(x, (a, b), args, len_args)

    plot = Plot(a, b)
    plot.draw_func(func, "Funkcja")
    plot.draw_func(approximation_polynomial, "Wielomian Interpolacyjny")
    plot.show()


if __name__ == "__main__":
    main()
