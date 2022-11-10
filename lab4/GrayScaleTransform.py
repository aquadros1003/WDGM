from BaseImage import *

class GrayScaleTransform(BaseImage):

        
    def __init__(self, path) -> None:
        super().__init__(path)

    def to_gray_without_overwrite(self):
        r, g, b = squeeze(dsplit(self.data, self.data.shape[-1]))

        r = r * 0.299 
        g = g * 0.587
        b = b * 0.114

        rows = self.data.shape[0]
        cols = self.data.shape[1]
        gray = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                gray[i][j] = (r[i][j] + g[i, j] + b[i, j])
        return gray

    def to_gray(self) -> BaseImage:

        self.data = self.to_gray_without_overwrite()
        self.color_model = 4
        return self

    def to_sepia(self, alpha_beta: tuple = (None, None), w: int = None) -> BaseImage:

        gray = self.to_gray_without_overwrite()

        if alpha_beta:
            alpha = alpha_beta[0]
            beta = alpha_beta[1]
            if (alpha + beta) > 2 or (alpha + beta) < 2 or alpha < 1 or beta > 1:
                print("Alpha\Beta out of range")
                return
            l0 = gray * alpha
            l0[l0 > 255] = 255
            l1 = gray
            l1[l1 > 255] = 255
            l2 = gray * beta
            l2[l2 > 255] = 255
        if w:
            if w < 20 or w > 40:
                print("w out of range")
                return
            l0 = gray + 2 * w
            l0[l0 > 255] = 255
            l1 = gray + w
            l1[l1 > 255] = 255
            l2 = gray
            l2[l2 > 255] = 255

        self.data = dstack((l0, l1, l2)).astype('uint8') 
        self.color_model = 5
        return self


    