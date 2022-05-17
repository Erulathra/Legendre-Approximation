import math
import os

from rich import print
from rich.console import Console
from rich.prompt import Prompt as prompt

import legendre_approximation as la
from charts import Plot


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


waiter_txt = "Wciśnij dowolny klawisz, aby kontynuować..."


functions = (lambda x: 0.7 * math.fabs(x),
             lambda x: 2 ** (math.cos(x)),
             lambda x: la.horner_scheme(x, [1, -1, 2, 4, -5, 1, 0, 1]),
             lambda x: math.sin(x),
             lambda x: math.sin(1/x) if x != 0 else 0)


function_name = ("0.7 * |x|",
                "2^(cos(x))",
                "x^7 - x^6 + 2x^5 + 4x^4 - 5x^3 + x^2 + 1",
                "sin(x)",
                "sin(1/x)")


class Range:
    def __init__(self) -> None:
        self.a = float()
        self.b = float()
    
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b
    
    def get(self):
        return (self.a, self.b)


class Legendre_args:
    def __init__(self) -> None:
        self.range = Range(-1, 1)
        self.epsilon = 0.005
        self.cotes_epsilon = 0.00001
        self.error_epsilon = 0.001
    
    def to_string(self):
        return f"Zakres: {self.range.get()}\n"\
             + f"Epsilon dla Lagrange'a: {self.epsilon}\n"\
             + f"Epsilon dla Newtona-Cotesa: {self.cotes_epsilon}\n"\
             + f"Epsilon błędu: {self.error_epsilon}"


def main():
    user_choice = ''
    function_index = 1
    args = Legendre_args()

    while user_choice != 'q':
        cls()
        print("\nWybrana funkcja: ", function_name[function_index])
        print(args.to_string(), "\n")
        print("Wybierz, czy chcesz:",
            "(1) Wybrać funkcję",
            "(2) Podać argumenty do aproksymacji",
            "(3) Obliczyć aproksymację",
            "[dim]\[q - wyjście][/]", sep="\n\t")
        user_choice = input("> ")
        print()
        match user_choice:
            case '1':
                function_index = choose_function(function_index) - 1
            case '2':
                args = choose_arguments(args)
            case '3':
                plot_charts(functions[function_index], args)


def choose_function(function_index) -> int:
    i = 1
    print(f"Wybierz funkcję [cyan]\[{function_index+1}][/]:")
    for name in function_name:
        print(f"\t({i}) {name}")
        i += 1
    choice = int(input("> ") or 0)
    return choice if 1 <= choice <= len(function_name) else function_index+1


def choose_arguments(args : Legendre_args) -> Legendre_args:
    approximation_range = prompt.ask("Wybierz zakres", default=f"{args.range.a} {args.range.b}")
    args.range.a, args.range.b = [float(item) for item in approximation_range.split()]

    args.epsilon = float(prompt.ask("Podaj epsilon dla Lagrange'a", default=str(args.epsilon)))
    args.cotes_epsilon = float(prompt.ask("Podaj epsilon dla Newtona-Cotesa", default=str(args.cotes_epsilon)))
    args.error_epsilon = float(prompt.ask("Podaj epsilon dla błędu", default=str(args.error_epsilon)))

    return args


def plot_charts(func, args : Legendre_args):
    try:
        print("[ Wciśnij Ctrl+C by przerwać obliczenia ]")
        legendre_args = la.legendre_approximation(func, args.range.get() , args.epsilon, args.cotes_epsilon, args.error_epsilon)
    except KeyboardInterrupt:
        prompt.ask(f"Przerwano działanie. {waiter_txt}")
        return
    print(legendre_args)

    console = Console()

    with console.status("[bold]Pracuję nad wynikiem...") as status:
        len_args = la.legendre_polynomial_arguments(len(legendre_args))
        def approximation_polynomial(x): return la.calculate_approximation_polynomial(x, args.range.get(), legendre_args, len_args)

    plot = Plot(args.range.a, args.range.b)
    plot.draw_func(func, "Funkcja")
    plot.draw_func(approximation_polynomial, "Wielomian Interpolacyjny")
    plot.show()


if __name__ == "__main__":
    main()
