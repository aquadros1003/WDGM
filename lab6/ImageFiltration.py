from typing import Optional
import numpy as np
from BaseImage import BaseImage

class ImageFiltration:
    def conv_channel(self, channel: np.ndarray, kernel: np.ndarray, prefix: Optional[float] = None) -> np.ndarray:
        """
        metoda wyrównująca histogram danego kanału
        """
        if prefix is None:
            prefix = 1
        new_channel = np.zeros((channel.shape[0], channel.shape[1]))
        for i in range(channel.shape[0]):
            for j in range(channel.shape[0]):
                for m in range(kernel.shape[0]):
                    for n in range(kernel.shape[0]):
                        new_channel[i, j] += channel[i - m, j -n] * kernel[m, n]
        new_channel = new_channel * prefix
        new_channel[new_channel > 255] = 255
        new_channel[new_channel < 0] = 0
        return new_channel.astype('uint8')

    def conv_2d(self, image: BaseImage, kernel: np.ndarray, prefix: Optional[float] = None) -> BaseImage:
        """
        metoda wyrównująca histogram obrazu
        """
        if prefix is None:
            prefix = 1
        if image.data.shape[-1] == 3:
            r = self.conv_channel(image.data[:, :, 0], kernel, prefix) 
            g = self.conv_channel(image.data[:, :, 1], kernel, prefix)
            b = self.conv_channel(image.data[:, :, 2], kernel, prefix)
            image.data = np.dstack((r, g, b))
        else:
            image.data = self.conv_channel(image.data, kernel, prefix)








        
        
        