import math
import legendre_approximation as la

from rich import print

functions = (lambda x: x ** (math.cos(x) - 1))


def main():
    test = la.legendre_polynomial(-0.9, 25)
    print(test)


if __name__ == "__main__":
    main()
