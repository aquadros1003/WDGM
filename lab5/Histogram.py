import numpy as np
import matplotlib.pyplot as plt

class Histogram:
    """
    klasa reprezentujaca histogram danego obrazu
    """
    values: np.ndarray  # atrybut przechowujacy wartosci histogramu danego obrazu

    def __init__(self, values: np.ndarray) -> None:
        if values.shape[-1] == 3:
            r = np.histogram(values[:, :, 0], bins = np.linspace(0, 255, 255))
            g = np.histogram(values[:, :, 1], bins = np.linspace(0, 255, 255))
            b = np.histogram(values[:, :, 2], bins = np.linspace(0, 255, 255))
            self.values = r + g + b
        else: 
            self.values = list(np.histogram(values, bins = np.linspace(0, 255, 255)))

    def to_cumulated(self) -> 'Histogram':
        """
        metoda zwracajaca histogram skumulowany na podstawie stanu wewnetrznego obiektu
        """
        self.values[0] = list(np.cumsum(self.values[0]))
        return self


    def plot(self) -> None:
        if len(self.values) == 6:
            r, g, b = self.values[0], self.values[2], self.values[4]
            x_r, x_g, x_b = self.values[1], self.values[3], self.values[5]
            r, g, b = np.append(r, [0]), np.append(g, [0]), np.append(b, [0])
            plt.plot(x_r, r, color = 'red', linewidth = 0.5)
            plt.plot(x_g, g, color = 'green', linewidth = 0.5)
            plt.plot(x_b, b, color = 'blue', linewidth = 0.5)
        else:
            x = np.append(self.values[0], [0])
            plt.plot(self.values[1], x, color = 'black', linewidth = 0.5)
        plt.xlim(0, 255)
        plt.title("Histogram") 
        plt.show()