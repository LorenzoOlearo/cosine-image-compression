import numpy as np
import scipy.fftpack as fft

import jpegDCT
import jpegUtils
from gui import GUI

from PIL import Image, ImageTk

from test.DCT import TestCosineTransform
from test.performance import run_test


class CosineImageCompression():

    def __init__(self, args, fast = True) -> None:
        self.gui = GUI(self)
        self.fast = fast
        
        if args.test:
            TestCosineTransform().run_test()
        if args.performance:
            run_test(lower=args.lower, upper=args.upper, iterations=args.iterations, load=args.load)
        if not args.nogui:
            self.gui.start()
            

    def dct(self, image, F, d):
        image = ImageTk.getimage(image).convert('L')

        image = np.asarray(image)

        return ImageTk.PhotoImage(Image.fromarray(jpegUtils.bitmap_to_jpeg(image, F, d, self.fast)))

        
