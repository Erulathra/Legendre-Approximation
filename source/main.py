import math

from rich import print
from rich.console import Console

import legendre_approximation as la
from charts import Plot

functions = (lambda x: 0.7 * math.fabs(x),
             lambda x: 2 ** (math.cos(x)),
             lambda x: la.horner_scheme(x, [1, -1, 2, 4, -5, 1, 0, 1]),
             lambda x: math.sin(x),
             lambda x: math.sin(1/x) if x != 0 else 0)


def main():
    func = functions[3]
    a, b = (-3, 5)
    # len_args = la.legendre_polynomial_arguments(100)
    # args = la.calculate_legendre_approximation(func, (a, b), len_args, 0.00001)
    args = la.legendre_approximation(func, (a, b), 0.08, 0.001, 0.01)
    print(args)

    console = Console()

    with console.status("[bold]Pracuję nad wynikiem...") as status:
        len_args = la.legendre_polynomial_arguments(len(args))
        def approximation_polynomial(x): return la.calculate_approximation_polynomial(x, (a, b), args, len_args)

    plot = Plot(a, b)
    plot.draw_func(func, "Funkcja")
    plot.draw_func(approximation_polynomial, "Wielomian Interpolacyjny")
    plot.show()


if __name__ == "__main__":
    main()
