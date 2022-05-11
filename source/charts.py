import numpy as np
from matplotlib import pyplot


class Plot:
    def __init__(self, minimum: float, maximum: float):
        self._figure: pyplot.Figure = pyplot.figure(dpi=200)
        self._axes: pyplot.Axes = self._figure.subplots()

        self._minimum = minimum
        self._maximum = maximum
        pyplot.grid()
        pyplot.xlabel('X')
        pyplot.ylabel('y')

    def draw_func(self, func, name: str):
        plot_x = np.linspace(self._minimum, self._maximum, 300)
        plot_y = np.zeros(300)

        for i in range(300):
            plot_y[i] = func(plot_x[i])

        self._axes.plot(plot_x, plot_y , label=name)

    def draw_points(self, X: np.ndarray, Y: np.ndarray):
        self._axes.scatter(X, Y, c="g")

    def show(self):
        self._axes.legend()
        self._figure.show()
