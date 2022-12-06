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
        channel = channel.astype(np.float64)
        rows, cols = self.data.shape[:2]
        max_value = np.max(channel)
        min_value = np.min(channel)
        if tail_elimination == True:
            max_value = np.percentile(channel, 95)
            min_value = np.percentile(channel, 5)
        for i in range(rows):
            for j in range(cols):
                try:
                    channel[i, j] = ((channel[i, j] - min_value) / (max_value - min_value)) * 255
                except ZeroDivisionError:
                    print("ZeroDivisionError")
        channel[channel > 255] = 255
        channel[channel < 0] = 0
        return channel.astype('uint8')

            

    def align_image(self, tail_elimination: bool = False) -> 'BaseImage':
        """
        metoda wyrównująca histogram obrazu
        """
        if self.data.shape[-1] == 3:
            r = self.align_channel(self.data[:, :, 0], tail_elimination)  
            g = self.align_channel(self.data[:, :, 1], tail_elimination)
            b = self.align_channel(self.data[:, :, 2], tail_elimination)
            self.data = np.dstack((r, g, b))
        else:
            self.data = self.align_channel(self.data, tail_elimination)
        return self


