import numpy as np
import scipy.fftpack as fft

import jpegDCT
import jpegUtils
from gui import GUI

from PIL import Image, ImageTk


class CosineImageCompression():

    def __init__(self, fast = True) -> None:
        self.gui = GUI(self)
        self.fast = fast
        self.gui.start()

    def dct(self, image, F, d):
        image = ImageTk.getimage(image).convert('L')

        image = np.asarray(image)

        return ImageTk.PhotoImage(Image.fromarray(jpegUtils.bitmap_to_jpeg(image, F, d, self.fast)))

        
