from BaseImage import * 

class ImageAligning(BaseImage):
    """
    klasa odpowiadająca za wyrównywanie hostogramu
    """
    def __init__(self, path) -> None:
        """
        inicjalizator ...
        """
        super().__init__(path)

    def align_channel(self, channel: np.ndarray, tail_elimination: bool = False) -> np.ndarray:
        """
        metoda wyrównująca histogram danego kanału
        """
        max_value = np.max(channel[0])
        min_value = np.min(channel[0])
        for pixel in channel[0]:
            pixel = pixel - min_value * 255 / (max_value - min_value).astype(np.uint8)
        return channel

    def align_image(self, tail_elimination: bool = True) -> 'BaseImage':
        """
        metoda wyrównująca histogram obrazu
        """
        if self.data.shape[-1] == 3:
            r = self.align_channel(self.data[:, :, 0], tail_elimination)
            g = self.align_channel(self.data[:, :, 1], tail_elimination)
            b = self.align_channel(self.data[:, :, 2], tail_elimination)
            self.data = np.stack((r, g, b), axis = -1)
        else:
            self.data = self.align_channel(self.data, tail_elimination)
        return self


