import numpy as np
import scipy.fftpack as fft

import jpegDCT
import jpegUtils
from gui import GUI


class CosineImageCompression():

    def __init__(self, fast = True) -> None:
        self.gui = GUI()
        self.fast = fast
        