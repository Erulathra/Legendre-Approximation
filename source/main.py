import math

from rich import print

import legendre_approximation as la
from charts import Plot

functions = (lambda x: 0.7 * math.fabs(x),
             lambda x: 2 ** (math.cos(x)),
             lambda x: x ** 3 - 2 * x + 4 * x - 10,
             lambda x: math.sin(x))


def main():
    func = functions[1]
    a, b = (-10, 10)
    args = la.legendre_approximation(func, (a, b), 40, 0.001)
    print(args)

    def approximation_polynomial(x): return la.calculate_approximation_polynomial(x, a, b, args)

    plot = Plot(a, b)
    plot.draw_func(func, "Funkcja")
    plot.draw_func(approximation_polynomial, "Wielomian Interpolacyjny")
    plot.show()


if __name__ == "__main__":
    main()
