from Histogram import Histogram
from BaseImage import BaseImage
from enum import Enum


class ImageDiffMethod(Enum):
    mse = 0
    rmse = 1

class ImageComparison(BaseImage):
    """
    Klasa reprezentujaca obraz, jego histogram oraz metody porównania
    """

    def histogram(self) -> Histogram:
        return Histogram(self.data)

    def to_gray(self) -> BaseImage:
        return super().to_gray()

    def to_gray_without_overwrite(self):
        return super().to_gray_without_overwrite()

    def compare_to(self, other: BaseImage, method: ImageDiffMethod) -> float:
        histogram1 = self.histogram()
        histogram2 = other.histogram()
        similarity = 0
        for pixel, pixel2 in zip(histogram1.values[0], histogram2.values[0]):
            similarity += (pixel - pixel2) ** 2
        similarity = similarity / len(histogram1.values)
        if method == 1:
            similarity = similarity ** (1/2)
        return similarity