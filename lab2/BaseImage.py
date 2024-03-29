from enum import Enum
from matplotlib.image import imread, imsave
from matplotlib.pyplot import imshow, axis
from numpy import cos, int16, ndarray, squeeze, dsplit, maximum, minimum, zeros, dstack, radians, float32
import numpy as np
from math import pi, sqrt, acos
from matplotlib.colors import hsv_to_rgb

class ColorModel(Enum):
    rgb = 0
    hsv = 1
    hsi = 2
    hsl = 3
    gray = 4  # obraz 2d

class BaseImage:
    data: ndarray
    color_model: ColorModel

    def __init__(self, path: str) -> None:
        self.data = imread(path)
        self.color_model = 0

    def save_img(self, path: str) -> None:
        imsave(path, self.data)

    def show_img(self) -> None:
        match self.color_model:
            case 0:
                imshow(self.data)
            case 1:
                imshow(hsv_to_rgb(self.data))
            case 2:
                imshow(hsv_to_rgb(self.data))
            case 3:
                imshow(hsv_to_rgb(self.data))
        axis('off')

    def get_layer(self, layer_id: int) -> ndarray:
        layer = squeeze(dsplit(self.data, self.data.shape[-1]))[layer_id]
        return layer

    def to_hsv(self) -> 'BaseImage' :

        r, g, b = squeeze(dsplit(self.data, self.data.shape[-1]))

        max_value = maximum(maximum(r, g), b)
        min_value = minimum(minimum(r, g), b)

        rows = self.data.shape[0]
        columns = self.data.shape[1]

        hue = zeros((rows, columns))
        saturation = zeros((rows, columns))
        value = zeros((rows, columns))

        for i in range(rows):
            for j in range(columns):
                value[i, j] = max_value[i, j] / 255

                if g[i, j] >= b[i, j]:
                    try:
                        hue[i, j] = int16(acos((int(r[i, j]) - int(g[i, j])/2 - int(b[i, j])/2) / sqrt(int(r[i, j])**2 + int(g[i, j])**2 + int(b[i, j])**2 - int(r[i, j])*int(g[i, j]) - int(r[i, j])*int(b[i, j]) - int(g[i, j])*int(b[i, j]) )) * 180/pi)
                    except ZeroDivisionError:
                        hue[i, j] = 0
                else: 
                    hue[i, j] = int16(360 - acos((int(r[i, j]) - int(g[i, j])/2 - int(b[i, j])/2) / sqrt(int(r[i, j])**2 + int(g[i, j])**2 + int(b[i, j])**2 - int(r[i, j])*int(g[i, j]) - int(r[i, j])*int(b[i, j]) - int(g[i, j])*int(b[i, j]) )) * 180/pi)
                
                if max_value[i, j] > 0:
                    saturation[i, j] = 1 - min_value[i, j]/max_value[i, j]
                else:
                    saturation[i, j] = 0

        self.data = dstack((hue, saturation, value))
        self.color_model = 1
        
        return self

    def to_hsi(self) -> 'BaseImage':
        r, g, b = float32(squeeze(dsplit(self.data, self.data.shape[-1])))

        min_value = minimum(minimum(r, g), b)
    
        rows = self.data.shape[0]
        columns = self.data.shape[1]

        hue = zeros((rows, columns))
        saturation = zeros((rows, columns))
        intensity = zeros((rows, columns))

        for i in range(rows):
            for j in range(columns):

                if g[i, j] >= b[i, j]:
                    try:
                        hue[i, j] = int16(acos((int(r[i, j]) - int(g[i, j])/2 - int(b[i, j])/2) / sqrt(int(r[i, j])**2 + int(g[i, j])**2 + int(b[i, j])**2 - int(r[i, j])*int(g[i, j]) - int(r[i, j])*int(b[i, j]) - int(g[i, j])*int(b[i, j]) )) * 180/pi)
                    except ZeroDivisionError:
                        hue[i, j] = 0
                else: 
                    hue[i, j] = int16(360 - acos((int(r[i, j]) - int(g[i, j])/2 - int(b[i, j])/2) / sqrt(int(r[i, j])**2 + int(g[i, j])**2 + int(b[i, j])**2 - int(r[i, j])*int(g[i, j]) - int(r[i, j])*int(b[i, j]) - int(g[i, j])*int(b[i, j]) )) * 180/pi)
                
                intensity[i, j] = ((r[i, j] + g[i, j] + b[i, j]) / 3.0)  #/ 255.0
                
                if intensity[i, j] > 0:
                    saturation[i, j] = 1 - min_value[i, j]/intensity[i, j]  #* 255.0)
                else:
                    saturation[i, j] = 0


        self.data = dstack((hue, saturation, intensity))
        self.color_model = 2
        return self 

    def to_hsl(self) -> 'BaseImage':

        r, g, b = squeeze(dsplit(self.data, self.data.shape[-1]))

        max_value = maximum(maximum(r, g), b)
        min_value = minimum(minimum(r, g), b)

        rows = self.data.shape[0]
        columns = self.data.shape[1]

        d = zeros((rows, columns))
        hue = zeros((rows, columns))
        saturation = zeros((rows, columns))
        lightness = zeros((rows, columns))

        for i in range(rows):
            for j in range(columns):
                d[i, j] = (max_value[i, j] - min_value[i, j]) / 255

                if g[i, j] >= b[i, j]:
                    try:
                        hue[i, j] = acos((int(r[i, j]) - int(g[i, j])/2 - int(b[i, j])/2) / sqrt(int(r[i, j])**2 + int(g[i, j])**2 + int(b[i, j])**2 - int(r[i, j])*int(g[i, j]) - int(r[i, j])*int(b[i, j]) - int(g[i, j])*int(b[i, j]) )) * 180/pi
                    except ZeroDivisionError:
                        hue[i, j] = 0     
                else: 
                    hue[i, j] = 360 - acos((int(r[i, j]) - int(g[i, j])/2 - int(b[i, j])/2) / sqrt(int(r[i, j])**2 + int(g[i, j])**2 + int(b[i, j])**2 - int(r[i, j])*int(g[i, j]) - int(r[i, j])*int(b[i, j]) - int(g[i, j])*int(b[i, j]) )) * 180/pi
                
                lightness[i, j] = 0.5*(int(max_value[i, j]) + int(min_value[i, j])) / 255
                
                if lightness[i, j] > 0:
                    saturation[i, j] = d[i, j] / (1 - abs(2 * lightness[i, j] - 1))
                else:
                    saturation[i, j] = 0

        self.data = dstack((hue, saturation, lightness))
        self.color_model = 3
        return self

    def to_rgb(self) -> 'BaseImage':
        rows = self.data.shape[0]
        columns = self.data.shape[1]
        r = zeros((rows, columns))
        g = zeros((rows, columns))
        b = zeros((rows, columns))

        match self.color_model:
            case 0:

                return self

            case 1:
                h, s, v = squeeze(dsplit(self.data, self.data.shape[-1]))

                max_value = v * 255
                min_value = zeros((rows, columns))
                z = zeros((rows, columns))

                for i in range(rows):
                    for j in range(columns):
                        min_value[i, j] = max_value[i, j] * (1 - s[i, j])
                        z[i, j] = (max_value[i, j] - min_value[i, j]) * (1 - abs((h[i, j] / 60)%2 - 1))
                        if h[i, j] >= 0 and h[i, j] < 60:
                            r[i, j] = int(max_value[i, j])
                            g[i, j] = int(z[i ,j] + min_value[i, j])
                            b[i, j] = int(min_value[i, j])
                        elif h[i, j] >= 60 and h[i ,j] < 120:
                            r[i, j] = int(z[i, j] + min_value[i, j])
                            g[i, j] = int(max_value[i, j])
                            b[i, j] = int(min_value[i, j])
                        elif h[i, j] >= 120 and h[i, j] < 180:
                            r[i, j] = int(min_value[i, j])
                            g[i, j] = int(max_value[i, j])
                            b[i, j] = int(z[i, j] + min_value[i ,j])
                        elif h[i, j] >= 180 and h[i, j] < 240:
                            r[i, j] = int(min_value[i, j])
                            g[i, j] = int(max_value[i, j])
                            b[i, j] = int(z[i, j] + min_value[i ,j])
                        elif h[i, j] >= 240 and h[i, j] < 300:
                            r[i, j] = int(z[i, j] + min_value[i ,j])
                            g[i, j] = int(min_value[i, j])
                            b[i, j] = int(max_value[i, j])
                        elif h[i, j] >= 300 and h[i, j] < 360:
                            r[i, j] = int(max_value[i, j])
                            g[i, j] = int(min_value[i, j])
                            b[i, j] = int(z[i, j] + min_value[i ,j])

            case 2:
                h, s, intensity = np.squeeze(np.dsplit(self.data, self.data.shape[-1]))

                for i in range(rows):
                    for j in range(columns):

                        if b[i, j] == g[i, j] == r[i, j]:
                            h[i, j] = 0
                    
                        if h[i, j] == 0:
                            r[i, j] = int(intensity[i, j] + 2*(intensity[i, j] * s[i, j]))
                            g[i, j] = int(intensity[i, j] - intensity[i, j] * s[i, j])
                            b[i, j] = int(intensity[i, j] - intensity[i, j] * s[i, j])

                        if 0 < h[i, j] < 120:
                            b[i, j] = int(intensity[i, j] * (1 - s[i, j]))
                            r[i, j] = int(intensity[i, j] * (1 + (s[i, j] * cos(radians(h[i, j]))) / cos(radians(60) - radians(h[i, j]))))
                            g[i, j] = int(3 * intensity[i, j] - (r[i, j] + b[i, j]))

                        if 120 < h[i, j] <= 240 or h[i, j] == 120:
                            r[i, j] = int(intensity[i, j] * (1 - s[i, j]))
                            g[i, j] = int(intensity[i, j] * (1 + (s[i, j] * cos(radians(h[i, j]))) / cos(np.radians(60) - radians(h[i, j]))))
                            b[i, j] = int(3 * intensity[i, j] - (r[i, j] + g[i, j]))

                        if 240 < h[i, j] <= 360 or h[i, j] == 240:
                            g[i, j] = int(intensity[i, j] * (1 - s[i, j]))
                            b[i, j] = int(intensity[i, j] * (1 + (s[i, j] * cos(radians(h[i, j]))) / cos(radians(60) - radians(h[i, j]))))
                            r[i, j] = int(3 * intensity[i, j] - (g[i, j] + b[i, j]))

                        elif r[i, j] > 255:
                            r[i, j] = 255

            case 3:
                h, s, l = squeeze(dsplit(self.data, self.data.shape[-1]))
                min_value = zeros((rows, columns))
                d = zeros((rows, columns))
                x = zeros((rows, columns))
                for i in range(rows):
                    for j in range(columns):
                        d[i, j] = s[i, j] * (1 - abs((2*l[i, j] - 1)))
                        min_value[i, j] = 255 * (l[i, j] - 0.5*d[i, j])
                        x[i, j] = d[i, j] * (1 - abs((h[i, j] / 60)%2 - 1))
                        if h[i, j] >= 0 and h[i, j] < 60:
                            r[i, j] = int(255 * d[i, j] + min_value[i, j])
                            g[i, j] = int(255 * x[i, j] + min_value[i, j])
                            b[i, j] = int(min_value[i, j])
                        elif h[i, j] >= 60 and h[i ,j] < 120:
                            r[i, j] = int(255 * x[i, j] + min_value[i, j])
                            g[i, j] = int(255 * d[i, j] + min_value[i, j])
                            b[i, j] = int(min_value[i, j])
                        elif h[i, j] >= 120 and h[i, j] < 180:
                            r[i, j] = int(min_value[i, j])
                            g[i, j] = int(255 * d[i, j] + min_value[i, j])
                            b[i, j] = int(255 * x[i, j] + min_value[i, j])
                        elif h[i, j] >= 180 and h[i, j] < 240:
                            r[i, j] = int(min_value[i, j])
                            g[i, j] = int(255 * x[i, j] + min_value[i, j])
                            b[i, j] = int(255 * d[i, j] + min_value[i, j])
                        elif h[i, j] >= 240 and h[i, j] < 300:
                            r[i, j] = int(255 * x[i, j] + min_value[i, j])
                            g[i, j] = int(min_value[i, j])
                            b[i, j] = int(255 * d[i, j] + min_value[i, j])
                        elif h[i, j] >= 300 and h[i, j] < 360:
                            r[i, j] = int(255 * d[i, j] + min_value[i, j])
                            g[i, j] = int(min_value[i, j])
                            b[i, j] = int(255 * x[i, j] + min_value[i, j])

        self.data = dstack((r, g, b)).astype('uint8')
        self.color_model = 0
        return self


