import math

from rich import print

import legendre_approximation as la
from charts import Plot

functions = (lambda x: 0.7 * math.fabs(x),
             lambda x: 2 ** (math.cos(x)),
             lambda x: x ** 3 - 2 * x + 4 * x - 10)


def main():
    func = functions[0]
    args = la.legendre_approximation(func, (-1, 1), 25, 0.00001)
    print(args)

    def approximation_polynomial(x): return la.calculate_approximation_polynomial(x, args)

    plot = Plot(-1, 1)
    plot.draw_func(func, "Funkcja")
    plot.draw_func(approximation_polynomial, "Wielomian Interpolacyjny")
    plot.show()


if __name__ == "__main__":
    main()
